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

# 3. Invoke-Command to get machine's OS version
$OSVersion = Invoke-Command -Session $Session -ScriptBlock{ 
                        return (Get-WmiObject win32_operatingsystem).Version;
                    }

# 4. Invoke-Command to get EP/Definition version  
if([System.Version]$OSVersion -ge [System.Version]'10.0.0.0')
{
    Write-Verbose "OS Windows 10 and newer detected."
    $Versions = Invoke-Command -Session $Session -ScriptBlock{
                        $EPVersion = (Get-MpComputerStatus).AMProductVersion;
                        $DefinitionVersion = (Get-MpComputerStatus).AntivirusSignatureVersion;
                            
                        return @($EPVersion, $DefinitionVersion);
                    }
}
else 
{
    Write-Verbose "old Windows detected" 
    $Versions = Invoke-Command -Session $Session -ScriptBlock{ 
                    $UninstallKey = "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall";
                    $ProductKeys = Get-ChildItem -Path $UninstallKey;
                    foreach($ProductKey in $ProductKeys)
                    {
                        $ProductPath = $ProductKey.Name.Replace("HKEY_LOCAL_MACHINE", "HKLM:");
                        $ProductName = (Get-ItemProperty $ProductPath).DisplayName;
                        if($ProductName -eq "System Center Endpoint Protection")
                        {
                            $EPVersion = (Get-ItemProperty $ProductPath).DisplayVersion;
                            break;
                        }
                    }

                    if($EPVersion)
                    {
                        $DefinitionVersion = (Get-ItemProperty "hklm:\SOFTWARE\Microsoft\Microsoft Antimalware\Signature Updates").ASSignatureVersion;  
                    }

                    return @($EPVersion, $DefinitionVersion);
                }
}

Remove-PSSession -Session $Session; # Close PS Session.

# 5. return a string array, null means no EP installed on machine 
#    otherwise, the first element is $EPVersion and the second one is $DefinitionVersion
return $Versions; 