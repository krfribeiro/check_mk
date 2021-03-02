# Monitor Windows Application Pools state 
# The alarm condition is to not have "Started" in state field - Valid until Windows Server 2012 - 2016 > Already brings new ways to administrate WebApplicationPools
# Get All Pools to iterate later
$AppPools = Get-WebAppPoolState
# Prints Check_MK Plugin Header                    
"<<<WebAppPool>>>"
# Loop for each application pool
ForEach($Item in $AppPools) 
{                
    $Name = ($Item.ItemXPath -Replace '(?:.*?)name=''([^'']*)(?:.*)', '$1').Trim()
	$Name = $Name -Replace ' ','_'
    $Status = ($item.Value).Trim()
    Write-Host " $Name $Status"
   } 