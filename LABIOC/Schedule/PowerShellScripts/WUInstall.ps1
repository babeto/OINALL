Param
(
    [Parameter(Mandatory = $True)]
    [String] $MachineName,

    [Parameter(Mandatory = $True)]
    [String] $Username,

    [Parameter(Mandatory = $True)]
    [String] $Password
)

# 1. New access credential($Credential) for machine
$SecuredPwd = ConvertTo-SecureString -String $Password -AsPlainText -Force;
$Credential = New-Object System.Management.Automation.PSCredential($Username, $SecuredPwd);

# 2. Try to establish PSSession to remote machine, if failed throw RemoteException
$Session = New-PSSession -ComputerName $MachineName -Credential $Credential;
if(!$?)
{
    throw [System.Management.Automation.RemoteException]"Could not access to [$MachineName] with username [$Username] and password [$Password]!";
}

Invoke-Command -Session $Session -ScriptBlock{

    #Get-Service;

    # set $Force to True will forcely update schedule task on a machine no matter whether it existsl

    
    $Unregister = $True

    $Force = $True


    $TaskName = "CMSEWindowsUpdate"

    $TaskExists = Get-ScheduledTask | Where-Object {$_.TaskName -like $TaskName}

    $Sys32Path = Join-Path -Path (Get-Item Env:\windir).value -ChildPath system32

    if(($Unregister -eq $True))
    {
        if($TaskExists)
        {
            Write-Host "Sheduled task exist and need Unregister, will Unregister task"
        
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$False
        }
    }
    elseif($TaskExists -and ($Force -ne $True))
    {
        Write-Host "Sheduled task exist and no Force update, will trigger task"
        
        Get-ScheduledTask -TaskName $TaskName | Start-ScheduledTask
    }
    else
    {
        Write-Host "Schedule task doesn't exist or need force update, will create task"

        $Version = Get-WmiObject -Class Win32_OperatingSystem | Select-Object -Property 'Version'

        Write-Host $Version.Version
        if([version]$Version.Version -lt [version]'10.0.0')
        {   
            Write-Host "OS under Windows 10"
            $action = New-ScheduledTaskAction -Execute 'wuauclt.exe' -Argument '/DetectNow /UpdateNow' -WorkingDirectory $Sys32Path
        }
        else
        {
            Write-Host "Windows 10 OS"
            $action = New-ScheduledTaskAction -Execute 'usoclient.exe' -Argument 'StartInstall' -WorkingDirectory $Sys32Path
        }

    
        $gettime = (Get-Date).AddMinutes(10)
        $run = $gettime.ToString('HH:mm')
    
        $trigger = New-ScheduledTaskTrigger -Once -At $run
        $principal = New-ScheduledTaskPrincipal -GroupId "BUILTIN\Administrators" -RunLevel Highest

        Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName "CMSEWindowsUpdate" -Description "Start a Windows Update scan and install Cycle" -Force
    }
}

Remove-PSSession -Session $Session; # Close PS Session.

