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

# 3. Invoke-Command to get hotfix list, including product hotfixes and OS hotfixes
$UpdateInformations = Invoke-Command -Session $Session -ScriptBlock{
                        $UpdateInfos=  @();

                        # Search product updates
                        $Searcher = New-Object -ComObject "Microsoft.Update.Searcher";
                        $Count = $Searcher.GetTotalHistoryCount();
                        $Updates = $Searcher.QueryHistory(0, $Count);                        
                        foreach($update in $Updates)
                        {
                            $Title = $update.Title
                            $regex = "[K|k][B|b]\d*"
                            try{
                                $KB = ($Title | Select-String -Pattern $regex).Matches[0].Value
							    $updateInfo = @{"HotfixID" = $KB; "Title" = $update.Title; "Date" = $update.Date };
							    $UpdateInfos += $updateInfo;
                            }
                            catch{
                                Out-Printer "null KB"
                            }
                        }

                        <# Search Windows OS updates
                        $WindowsHotfixes = Get-WmiObject -Query "Select * from Win32_QuickFixEngineering";
                        foreach($windowsHotfix in $WindowsHotfixes)
                        {
							$Title = $windowsHotfix.Description + " For Microsoft Windows " + $KB;
							$updateInfo = @{"HotfixID" = $windowsHotfix.HotFixID; "Title" = $Title; "Date" = $windowsHotfix.InstalledOn; "IsQFE" = true };
							$UpdateInfos += $updateInfo;
                        }
                        #>
                        return $UpdateInfos;
                    }

Remove-PSSession -Session $Session; # Close PS Session.

# 4. return a Json string
return ConvertTo-Json -InputObject $UpdateInformations; 