#!/bin/bash

# Define your NAS devices and corresponding SSH credentials
nas_devices=(
    "nas1.example.com:username1:password1"
    "nas2.example.com:username2:password2"
    # Add more NAS devices in the same format if needed
)

# Function to execute SSH commands on NAS
function execute_ssh_command() {
    local address=$1
    local username=$2
    local password=$3
    local command=$4

    # Print NAS URL
    echo "Connecting to NAS: $address"

    # Execute command and store the result, filter only for /volume1 data
    sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$username@$address" "$command" | grep '/volume1'
}

# Loop through each NAS device and execute df -h command
for device_info in "${nas_devices[@]}"; do
    IFS=':' read -r address username password <<< "$device_info"
    echo "Executing df -h on NAS: $address"
    execute_ssh_command "$address" "$username" "$password" "df -h"
    echo "Logged out of NAS: $address"
done

