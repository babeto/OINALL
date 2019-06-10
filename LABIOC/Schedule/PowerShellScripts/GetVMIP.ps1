Param
(
    [Parameter(Mandatory = $True)]
    [String] $MachineName,

    [Parameter(Mandatory = $True)]
    [String] $Username,

    [Parameter(Mandatory = $True)]
    [String] $Password,

	[Parameter(Mandatory = $True)]
    [String] $VMName
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

# 2. Get VM's IP
$IPS = Invoke-Command -Session $Session -ScriptBlock { 
    param($VMName)
    return (Get-VM -Name $VMName | Get-VMNetworkAdapter).ipAddresses;
    } -Args $VMName
Remove-PSSession -Session $Session; # Close PS Session.
return $IPS;