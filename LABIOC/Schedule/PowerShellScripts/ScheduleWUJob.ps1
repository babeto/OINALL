Param
(
    [Parameter(Mandatory = $True)]
    [String] $MachineName,

    [Parameter(Mandatory = $True)]
    [String] $Username,

    [Parameter(Mandatory = $True)]
    [String] $Password

)

$ScriptContent = Get-Content $PSScriptRoot\WUJob.ps1

$BatContent = Get-Content $PSScriptRoot\RunWUJob.bat

$DNSResetContent = Get-Content $PSScriptRoot\DNSReset.bat

# 1. New access credential($Credential) for machine
$SecuredPwd = ConvertTo-SecureString -String $Password -AsPlainText -Force;
$Credential = New-Object System.Management.Automation.PSCredential($Username, $SecuredPwd);

# 2. Try to establish PSSession to remote machine, if failed throw RemoteException
$Session = New-PSSession -ComputerName $MachineName -Credential $Credential;
if(!$?)
{
    throw [System.Management.Automation.RemoteException]"Could not access to [$MachineName] with username [$Username] and password [$Password]!";
}

Invoke-Command -Session $Session  -ScriptBlock{

    #Get-Service;

    # set Unregister to True if you want register this task, and will clean all related files

    $Unregister = $False

    # set $Force to True will forcely update schedule task on a machine no matter whether it existsl

    $Force = $False

    $TaskName = "CMSEPSWindowsUpdate"

    

    $Sys32Path = Join-Path -Path (Get-Item Env:\windir).value -ChildPath system32

    $PSWUJobDir = (Get-Item Env:\SystemDrive).value + "\" + "CMSEPSWindowsUpdate"

    $PSWUJobScript = $PSWUJobDir + "\" + "WUJob.ps1"

    $PSWUJobBat = $PSWUJobDir + "\" + "RunWUJob.bat"

	$PSDNSResetBat = $PSWUJobDir + "\" + "DNSReset.bat"


    $winVersion = Get-WmiObject -Class Win32_OperatingSystem | Select-Object -Property "Version"


    if([version]$winVersion.Version -lt [version]"6.2.0")
    {
        # windows under Windows8/2012 doesn't support *-ScheduleTask, use SCHTASKS instead
        $TaskExists = SCHTASKS /Query /TN $TaskName
    }
    elseif([version]$winVersion.Version -ge [version]"6.2.0")
    {
        # set source to Microsoft Update
        $TaskExists = Get-ScheduledTask | Where-Object {$_.TaskName -like $TaskName}

    }


    if($Unregister -eq $True)
    {
        if($TaskExists)
        {
            Write-Output "Switch to unregister task and clean files"
            

                if([version]$winVersion.Version -lt [version]"6.2.0")
                {
                    # windows under Windows8/2012 doesn't support *-ScheduleTask, use SCHTASKS instead
                    SCHTASKS /Delete /TN $TaskName /F
                }
                elseif([version]$winVersion.Version -ge [version]"6.2.0")
                {
                    # set source to Microsoft Update
                    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$False

                }
            

            Remove-Item -Path $PSWUJobDir -Recurse

        }
    }
    elseif($TaskExists -and ($Force -ne $True))
    {
        Write-Host "Sheduled task exist and no Force update, will trigger task"
        
                if([version]$winVersion.Version -lt [version]"6.2.0")
                {
                    # windows under Windows8/2012 doesn't support *-ScheduleTask, use SCHTASKS instead
                    SCHTASKS /Run /TN $TaskName
                }
                elseif([version]$winVersion.Version -ge [version]"6.2.0")
                {
                    # set source to Microsoft Update
                    Get-ScheduledTask -TaskName $TaskName | Start-ScheduledTask
                }

    }
    else
    {
        Write-Host "Schedule task doesn't exist or need force update, will create the task "

        New-Item $PSWUJobDir -ItemType directory -Force

        New-Item $PSWUJobScript -ItemType file -Force

        Set-Content -Path $PSWUJobScript -value $Using:ScriptContent

        New-Item $PSWUJobBat -ItemType file -Force

        Set-Content -Path $PSWUJobBat -Value $Using:BatContent

		New-Item $PSDNSResetBat -ItemType file -Force

        Set-Content -Path $PSDNSResetBat -Value $Using:DNSResetContent

                if([version]$winVersion.Version -lt [version]"6.2.0")
                {
                    # windows under Windows8/2012 doesn't support *-ScheduleTask, use SCHTASKS instead
                    SCHTASKS /Create /TN $TaskName /RU "NT AUTHORITY\SYSTEM" /SC ONSTART /RL HIGHEST /TR "cmd /c $PSWUJobBat" /DELAY 0005:00 /F
                }
                elseif([version]$winVersion.Version -ge [version]"6.2.0")
                {
                    # set source to Microsoft Update
                    $actinArgs = "/c $PSWUJobBat"

                    $action = New-ScheduledTaskAction -Execute 'cmd' -Argument $actinArgs -WorkingDirectory $PSWUJobDir

                    $gettime = (Get-Date).AddMinutes(60)
                    $run = $gettime.ToString('HH:mm')

                    $setting = New-ScheduledTaskSettingsSet -Hidden
                    $trigger = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-Timespan -Minutes 10)
                    $principal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest

                    Register-ScheduledTask -Action $action -Trigger $trigger -Settings $setting -Principal $principal -TaskName $TaskName  -Description "Start a Windows Update scan and install Cycle" -Force
                }
        
        
    }
}

Remove-PSSession -Session $Session; # Close PS Session.

