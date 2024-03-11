function Post-DiskUsage {
    # Get current date and time
    $CurrentDateTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # Get disk usage information for all drives
    $diskUsage = Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, VolumeName, @{Name="Size(GB)"; Expression={[math]::Round($_.Size / 1GB, 2)}}, @{Name="FreeSpace(GB)"; Expression={[math]::Round($_.FreeSpace / 1GB, 2)}}, @{Name="UsedSpace(GB)"; Expression={[math]::Round(($_.Size - $_.FreeSpace) / 1GB, 2)}}

    # Define API endpoint
    $apiUrl = "http://localhost:5000/api/disk"

    foreach ($disk in $diskUsage) {
        $diskData = @{
            "date" = $CurrentDateTime
            "device_id" = $disk.DeviceID
            "volume_name" = $disk.VolumeName
            "size" = $disk.'Size(GB)'
            "free_space" = $disk.'FreeSpace(GB)'
            "used_space" = $disk.'UsedSpace(GB)'
        }

        # Convert data to JSON
        $jsonData = $diskData | ConvertTo-Json

        # Invoke REST API to post disk data
        Invoke-RestMethod -Uri $apiUrl -Method Post -Body $jsonData -ContentType "application/json"
    }

    Write-Host "Disk usage information has been posted to the API"
}

# Invoke the function to post disk usage information to the API
Post-DiskUsage

