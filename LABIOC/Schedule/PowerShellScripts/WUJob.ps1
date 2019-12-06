# set to true will force reboot request after Update applied
$AutoReboot = $true



# check if the WU Installer is busy


$objInstaller = New-Object -ComObject "Microsoft.Update.Installer"

Switch($objInstaller.IsBusy)
{
    $true { Write-Output "Installer is busy, will quit this time"; return }
}

$objSystemInfo = New-Object -ComObject "Microsoft.Update.SystemInfo"

Switch($objSystemInfo.RebootRequired)
{
    $true { Write-Output "Reboot is required, Reboot computer"
            Restart-Computer -Force
            }
}


# Set Update Source to sync updates


$objServiceManager = New-Object -ComObject "Microsoft.Update.ServiceManager"

$objSession = New-Object -ComObject "Microsoft.Update.Session"

$objSearcher = $objSession.CreateUpdateSearcher()


$winVersion = Get-WmiObject -Class Win32_OperatingSystem | Select-Object -Property "Version"

if([version]$winVersion.Version -lt [version]"10.0.0")
{
    # set source to Windows Update

    Write-Output "version below Windows 10"
    Write-Debug "Set source of updates to Windows Update"
    $objSearcher.ServerSelection = 2
    #$objSearcher.ServiceID = "9482F4B4-E343-43B6-B170-9A65BC822C77"
    $serviceName = "Windows Update"
}
elseif([version]$winVersion.Version -ge [version]"10.0.0")
{
    # set source to Microsoft Update

    Write-Output "version above Windows 10"
    Write-Debug "Set source of updates to Microsoft Update"

    $objServiceManager.AddService2("7971f918-a847-4430-9279-4a52d1efe18d",7,"")

    $objSearcher.ServerSelection = 3
    $objSearcher.ServiceID = "7971f918-a847-4430-9279-4a52d1efe18d"
    $serviceName = "Microsoft Update"
}

Write-Verbose "Set source of update to $serviceName..."

##Search Update List

try
{
    $search = "IsInstalled = 0"
    $search += " and IsHidden = 0"
    
    Write-Output "search criterea $search"

    $objResults = $objSearcher.Search($search)

}
catch
{

    if ($_ -match "HRESULT: 0x80072EE2")
    {
        Write-Warning "HRESULT: 0x80072EE2, Maybe you don't have connection to Windows Update Server"
    }
	elseif ($_ -match "HRESULT: 0x8024402C")
    {
		$PSScriptPath = split-path -parent $MyInvocation.MyCommand.Definition
        Write-Warning "HRESULT: 0x8024402C, Maybe you don't have connection to Windows Update Server"
		cmd /c $PSScriptPath\DnsReset.bat
    }
    else
    {
        Write-Error $_ -ErrorAction Stop
    }
    return
}

$objCollectionUpdate = New-Object -ComObject "Microsoft.Update.UpdateColl"

$NumberOfUpdate = 1
$UpdatesExtraDataCollection = @{}
$PreFoundUpdatesToDownLoad = $objResults.Updates.count

if($PreFoundUpdatesToDownLoad -eq 0)
{
    Write-Output "Not found any updates in pre search criteria"
    return
}

Foreach($Update in $objResults.Updates)
{
    # a flag to determine if add the update to download list,
    # may be useful later, but for now we don't have any filter condition
    # and will search all updates
    $UpdateAccess = $true

    $objCollectionUpdate.Add($Update)

    $UpdatesExtraDataCollection.Add($Update.Identity.UpdateID,@{KB = $KB; Size = $size})

    $NumberOfUpdate++
}

$FoundUpdatesToDownload = $objCollectionUpdate.count

Write-Output "found $FoundUpdatesToDownload updates to download"

if($FoundUpdatesToDownload -eq 0)
{
    Write-Warning "Not Found any updates in Search Criteria to download"
    return
}

#Choose Update to download

$NumberOfUpdate = 1
$logCollection = @()

$objCollectionChoose = New-Object -ComObject "Microsoft.Update.UpdateColl"

Foreach($Update in $objCollectionUpdate)
{
    if($update.EulaAccepted -eq 0)
    {
        Write-Output "Accept Eula"
        $Update.AcceptEula()
    }

    $objCollectionChoose.Add($Update)

    $log = New-Object PSObject -Property @{
            Title = $Update.Title
            KB = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].KB
			Size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
			Status = $Status
			X = 2
            }

    $log.PSTypeNames.Clear()
	$log.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
				
	$logCollection += $log

    $NumberOfUpdate++
}

Write-Output "Choose update completed"

Write-Output "log Collection"
$logCollection


$AcceptUpdatesToDownload = $objCollectionChoose.count

Write-Output "Accept $AcceptUpdatesToDownload Updates to download"

if($AcceptUpdatesToDownload -eq 0)
{

Write-Warning "Not Accept any Updates to download"
return

}

## Download Updates

Write-Output "Start download updates"

$NumberOfUpdate = 1

$objcollectionDownload = New-Object -ComObject "Microsoft.Update.UpdateColl"

Foreach($Update in $objCollectionChoose)
			{
               "[$NumberOfUpdate/$AcceptUpdatesToDownload] $($Update.Title) $size"
				Write-Progress -Activity "[3/$NumberOfStage] Downloading updates" -Status "[$NumberOfUpdate/$AcceptUpdatesToDownload] $($Update.Title) $size" -PercentComplete ([int]($NumberOfUpdate/$AcceptUpdatesToDownload * 100))
				Write-Debug "Show update to download: $($Update.Title)"
				
				Write-Debug "Send update to download collection"
				$objCollectionTmp = New-Object -ComObject "Microsoft.Update.UpdateColl"
				$objCollectionTmp.Add($Update) | Out-Null
					
				$Downloader = $objSession.CreateUpdateDownloader() 
				$Downloader.Updates = $objCollectionTmp
				Try
				{
					Write-Debug "Try download update"
					$DownloadResult = $Downloader.Download()
				} #End Try
				Catch
				{
					If($_ -match "HRESULT: 0x80240044")
					{
						Write-Warning "Your security policy don't allow a non-administator identity to perform this task"
					} #End If $_ -match "HRESULT: 0x80240044"
					
					Return
				} #End Catch 
				
				Write-Debug "Check ResultCode"
				Switch -exact ($DownloadResult.ResultCode)
				{
					0   { $Status = "NotStarted" }
					1   { $Status = "InProgress" }
					2   { $Status = "Downloaded" }
					3   { $Status = "DownloadedWithErrors" }
					4   { $Status = "Failed" }
					5   { $Status = "Aborted" }
				} #End Switch
				
				Write-Debug "Add to log collection"
				$log = New-Object PSObject -Property @{
					Title = $Update.Title
					KB = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].KB
					Size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
					Status = $Status
					X = 3
				} #End PSObject Property
				
				$log.PSTypeNames.Clear()
				$log.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
				
				$log
				
				If($DownloadResult.ResultCode -eq 2)
				{
					Write-Debug "Downloaded then send update to next stage"
					$objCollectionDownload.Add($Update) | Out-Null
				} #End If $DownloadResult.ResultCode -eq 2
				
				$NumberOfUpdate++
				
			} #End Foreach $Update in $objCollectionChoose
			Write-Progress -Activity "[3/$NumberOfStage] Downloading updates" -Status "Completed" -Completed

			$ReadyUpdatesToInstall = $objCollectionDownload.count
			Write-Verbose "Downloaded [$ReadyUpdatesToInstall] Updates to Install"
		
			If($ReadyUpdatesToInstall -eq 0)
			{
				Write-Warning "Don't found any downloaded Updates to Install"
				Return
			} #End If $ReadyUpdatesToInstall -eq 0
		



Write-Debug "STAGE 4: Install updates"
				$NeedsReboot = $false
				$NumberOfUpdate = 1
				
				#install updates	
				Foreach($Update in $objCollectionDownload)
				{   
                    
					Write-Progress -Activity "[4/$NumberOfStage] Installing updates" -Status "[$NumberOfUpdate/$ReadyUpdatesToInstall] $($Update.Title)" -PercentComplete ([int]($NumberOfUpdate/$ReadyUpdatesToInstall * 100))
					Write-Debug "Show update to install: $($Update.Title)"
					
					Write-Debug "Send update to install collection"
					$objCollectionTmp = New-Object -ComObject "Microsoft.Update.UpdateColl"
					$objCollectionTmp.Add($Update) | Out-Null
					
					$objInstaller = $objSession.CreateUpdateInstaller()
					$objInstaller.Updates = $objCollectionTmp
						
					Try
					{
						Write-Debug "Try install update"
						$InstallResult = $objInstaller.Install()
					} #End Try
					Catch
					{
						If($_ -match "HRESULT: 0x80240044")
						{
							Write-Warning "Your security policy don't allow a non-administator identity to perform this task"
						} #End If $_ -match "HRESULT: 0x80240044"
						
						Return
					} #End Catch
					
					If(!$NeedsReboot) 
					{ 
						Write-Debug "Set instalation status RebootRequired"
						$NeedsReboot = $installResult.RebootRequired 
					} #End If !$NeedsReboot
					
					Switch -exact ($InstallResult.ResultCode)
					{
						0   { $Status = "NotStarted"}
						1   { $Status = "InProgress"}
						2   { $Status = "Installed"}
						3   { $Status = "InstalledWithErrors"}
						4   { $Status = "Failed"}
						5   { $Status = "Aborted"}
					} #End Switch
				   
					Write-Debug "Add to log collection"
					$log = New-Object PSObject -Property @{
						Title = $Update.Title
						KB = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].KB
						Size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
						Status = $Status
						X = 4
					} #End PSObject Property
					
					$log.PSTypeNames.Clear()
					$log.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
					
					$log
				
					$NumberOfUpdate++
				} #End Foreach $Update in $objCollectionDownload
				Write-Progress -Activity "[4/$NumberOfStage] Installing updates" -Status "Completed" -Completed
				


				If($NeedsReboot)
				{
					If($AutoReboot)
					{
						Restart-Computer -Force
					} #End If $AutoReboot
					Else
					{
						$Reboot = Read-Host "Reboot is required. Do it now ? [Y/N]"
						If($Reboot -eq "Y")
						{
							Restart-Computer -Force
						} #End If $Reboot -eq "Y"
						
					} #End Else $IgnoreReboot	
					
				} #End If $NeedsReboot
