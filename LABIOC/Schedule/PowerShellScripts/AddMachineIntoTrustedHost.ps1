Param
(
    [Parameter(Mandatory = $True)]
    [String] $MachineName
)

$preTrustedList = (Get-Item wsman:localhost\client\trustedhosts).Value.Trim().ToLower()
if($preTrustedList -eq "*")
{
}
elseif([String]::IsNullOrEmpty($preTrustedList))
{
    Set-Item wsman:localhost\client\trustedhosts -Value $MachineName -Force;
}
elseif($preTrustedList.Split(',') -notcontains $MachineName.Trim().ToLower())
{
    Set-Item wsman:localhost\client\trustedhosts -Value ($preTrustedList + ',' + $MachineName) -Force;
}
Get-Item wsman:localhost\client\trustedhosts