function Log-MACAddress {
    # Set the fixed name variable
    $name = "YourFixedNameHere"

    # Define the API endpoint URL
    $apiUrl = "http://localhost:5000/api/item"

    # Get all network adapters and loop through each one
    $networkAdapters = Get-NetAdapter
    foreach ($adapter in $networkAdapters) {
        # Get the MAC address and interface description
        $macAddress = $adapter.MacAddress
        $interface = $adapter.InterfaceDescription

        # Check if MAC address has appeared before
        $existingMacAddresses = (Invoke-RestMethod -Uri $apiUrl).mac_address
        if ($existingMacAddresses -contains $macAddress) {
            $appearBefore = "Yes"
        } else {
            $appearBefore = "No"
        }

        # Perform ping test
        $pingResult = "Failed"
        if (Test-Connection -ComputerName 1.1.1.1 -Count 3 -Quiet) {
            $pingResult = "Success"
        }

        # Define the data payload
        $data = @{
            "name" = $name
            "mac_address" = $macAddress
            "appear_before" = $appearBefore
            "interface" = $interface
            "internet" = $pingResult
        }

        # Invoke the API to add data
        Invoke-RestMethod -Uri $apiUrl -Method Post -Body ($data | ConvertTo-Json) -ContentType "application/json"
    }

    Write-Host "Script finished"
}

Log-MACAddress

