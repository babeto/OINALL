
Import-Module Az

#$contextpath = Resolve-Path .\Context.json

Import-AzContext -Path 'C:\repos\OINALL\LABIOC\Schedule\PowerShellScripts\Context.json' |Out-Null

$ResourceList = New-Object -TypeName System.Collections.ArrayList 

$subs = Get-AzSubscription

foreach( $sub in $subs)
{
    Select-AzSubscription -SubscriptionId $sub.Id
    #Write-Output $sub.Name
    
    $Resource = Get-AzResource -ResourceType Microsoft.Compute/virtualMachines
    

    #$AllResource.Add($sub.Name, $Resource)
    if($Resource -ne $null) {
        $ResourceList += $Resource
    }

    #$Resource |  Format-Table -AutoSize
}

# $Resource = Get-AzResource -ResourceType Microsoft.Compute/virtualMachines

$ResourceList |  ConvertTo-Json |Out-Host

 
 #return $AllMachines
 
<#
$html=$null
$i=0

 $html2=$ResourceList | Select-Object | select ResourceName, ResourceGroupName | ConvertTo-Html

$ResourceList.Count
Foreach($res in $ResourceList)
{
if($i -eq 0)
 {
    $i
    $output=$res | select ResourceName, ResourceGroupName | ConvertTo-Html | Select-Object -SkipLast 2
    $html=$html+$output
    $i++
 }
 if($i -eq $ResourceList.Count)
 {
    $i
    $output=$res | select ResourceName, ResourceGroupName | ConvertTo-Html | Select-Object -Skip 6
    $html=$html+$output
    $i++
 }
 else
 {
    $i
    $output=$res | select ResourceName, ResourceGroupName| ConvertTo-Html | Select-Object -Skip 6| Select-Object -SkipLast 2
    $html=$html+$output
    $i++
 }

}


$htmlPath = (Join-Path C:\Users\v-alhuan\Documents  Result.html)
$html2 |Out-File $htmlPath

&(join-path C:\Users\v-alhuan\Documents "\tool\EmailSender.exe") /emailSubject "AzureVMs" /emailBodyFile $htmlPath


#>