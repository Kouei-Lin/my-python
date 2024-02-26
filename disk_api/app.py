import requests

# Make a GET request to the API endpoint
response = requests.get('http://127.0.0.1:5000/api/disk-usage')

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the disk usage information returned by the API
    data = response.json()
    print("Total disk space:", data['total'])
    print("Used disk space:", data['used'])
    print("Free disk space:", data['free'])
else:
    # Print an error message if the request was not successful
    print("Error:", response.status_code)

