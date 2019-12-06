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
    $TaskName = "CMSEWindowsUpdate"

    $TaskExists = Get-ScheduledTask | Where-Object {$_.TaskName -like $TaskName}

    if($TaskExists)
    {
        Write-Host "Sheduled task exist, will trigger task"
        
        Get-ScheduledTask -TaskName $TaskName | Start-ScheduledTask
    }
    else
    {
        Write-Host "Schedule task doesn't exist, will create task"

        $Version = Get-WmiObject -Class Win32_OperatingSystem | Select-Object -Property 'Version'

        Write-Host $Version.Version
        if($Version.Version -lt [version]'10.0.0')
        {   
            Write-Host "OS under Windows 10"
            $action = New-ScheduledTaskAction -Execute 'cmd /c C:\Windows\system32\wuauclt.exe /DetectNow /UpdateNow'
        }
        else
        {
            Write-Host "Windows 10 OS"
            $action = New-ScheduledTaskAction -Execute 'cmd /c C:\Windows\system32\usoclient.exe startscan'
        }

    
        $gettime = (Get-Date).AddMinutes(1)
        $run = $gettime.ToString('HH:mm')
    
        $trigger = New-ScheduledTaskTrigger -Once -At $run
        $principal = New-ScheduledTaskPrincipal -GroupId "BUILTIN\Administrators" -RunLevel Highest

        Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName "CMSEWindowsUpdate" -Description "Calll a Windows Update Cycle"
    }
}

Remove-PSSession -Session $Session; # Close PS Session.



return $IPS;