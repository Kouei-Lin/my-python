#!/bin/bash

# Define your NAS devices and corresponding SSH credentials
nas_devices=(
    "user@192.168.xxx.xxx:password"
    # Add more NAS devices in the same format if needed
)

# Flask API endpoint
api_endpoint="http://your-api-host/api/nas"

# Function to execute SSH commands on NAS
function execute_ssh_command() {
    local address=$1
    local username=$2
    local password=$3
    local command=$4

    # Execute command and store the result
    sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$username@$address" "$command"
}

# Function to calculate CPU usage
function calculate_cpu_usage() {
    local idle_old=$(grep 'cpu ' /proc/stat | awk '{print $5}')
    local total_old=0
    local cpu_usage=0

    # Sum of all CPU time values
    for value in $(grep 'cpu ' /proc/stat | awk '{for(i=2;i<=NF;i++) sum += $i}; END {print sum}'); do
        total_old=$((total_old + value))
    done

    # Sleep for 1 second to calculate difference
    sleep 1

    local idle_new=$(grep 'cpu ' /proc/stat | awk '{print $5}')
    local total_new=0

    # Sum of all CPU time values after 1 second
    for value in $(grep 'cpu ' /proc/stat | awk '{for(i=2;i<=NF;i++) sum += $i}; END {print sum}'); do
        total_new=$((total_new + value))
    done

    # Calculate CPU usage percentage
    local diff_idle=$((idle_new - idle_old))
    local diff_total=$((total_new - total_old))
    cpu_usage=$((100 * (diff_total - diff_idle) / diff_total))

    echo "$cpu_usage"
}

# Function to generate JSON data for NAS with CPU and RAM usage
function generate_json() {
    local address=$1
    local disk_usage=$2
    local cpu_usage=$3
    local ram_usage=$4
    local total_disk=$5
    local used_disk=$6

    cat <<EOF
{
  "ip": "$address",
  "disk_usage": "$disk_usage",
  "cpu_usage": "$cpu_usage",
  "ram_usage": "$ram_usage",
  "total_disk": "$total_disk",
  "used_disk": "$used_disk"
}
EOF
}

# Loop through each NAS device and execute commands to retrieve disk, CPU, RAM, total disk, and used disk usage
for device_info in "${nas_devices[@]}"; do
    IFS=':' read -r address username password <<< "$device_info"
    echo "Executing commands on NAS: $address"

    # Execute command to retrieve disk usage
    disk_usage=$(execute_ssh_command "$address" "$username" "$password" "df -h /volume1 | awk 'NR==2 {print \$5}' | cut -d'%' -f1")

    # Execute command to retrieve total and used disk space
    disk_info=$(execute_ssh_command "$address" "$username" "$password" "df -h /volume1 --output=size,used | awk 'NR==2 {print \$1, \$2}'")
    read -r total_disk used_disk <<< "$disk_info"

    # Calculate CPU usage
    cpu_usage=$(calculate_cpu_usage)

    # Execute command to retrieve RAM usage
    ram_usage=$(execute_ssh_command "$address" "$username" "$password" "free | grep Mem | awk '{print \$3/\$2 * 100}'")

    # Generate JSON data with dynamically retrieved disk, CPU, RAM, total disk, and used disk usage
    json_data=$(generate_json "$address" "$disk_usage" "$cpu_usage" "$ram_usage" "$total_disk" "$used_disk")

    # Post JSON data to the Flask API
    curl -X POST -H "Content-Type: application/json" -d "$json_data" "$api_endpoint"

    echo "Data posted to API for NAS: $address"
done

