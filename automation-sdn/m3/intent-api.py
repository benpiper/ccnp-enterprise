# Import the Python libraries we'll need to use the Intent API

import json
import requests
from requests.auth import HTTPBasicAuth

# Obtain an authentication token to use in future API requests
# Username: devnetuser
# Password: Cisco123!

response = requests.post("https://sandboxdnac.cisco.com/api/system/v1/auth/token", \
    auth = HTTPBasicAuth("devnetuser","Cisco123!"))

# The response code HTTP 200 OK indicates successful authentication

response

# View the response in JSON format

response.json()

# The response JSON contains a key/value pair
# "Token" is the key and the long random string is the token
# value which we'll store in the variable named "token"

token = response.json()["Token"]

# We have to pass the token value using the "x-auth-token" HTTP header
# Create the headers from JSON

headers = {
              'x-auth-token': response.json()["Token"]
          }

# Use the "network-device" API to get information on network devices

url="https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"

# Send a GET request

response = requests.get(url, headers=headers)

# The response body is in JSON and it's long, making it difficult to read.
# We'll clean it up a bit using the json.dumps function.
print(json.dumps(response.json(), indent=2))

# We can get detailed information on a device by its IP address

url="https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/ip-address/10.10.20.51"
response = requests.get(url, headers=headers)
print(json.dumps(response.json(), indent=2))

# HTTP Response codes

# You want to see an HTTP response code that begins with 2xx
# But had we used invalid credentials, we would've
# seen an "HTTP 401 Not Authenticated" error

response401 = requests.post("https://sandboxdnac.cisco.com/api/system/v1/auth/token", \
    auth=HTTPBasicAuth("devnetuser","wrongpassword"))
response401

# The response text gives us another clue

response401.text

# Trying to call the API without specifying a valid token also yields a 401 response
# The following request leaves out the headers that should contain the authentication token

requests.get(url)
requests.get(url).text

# If you accidentally call a non-existent API, you get an "HTTP 404 Not Found" error

wrongurl="https://sandboxdnac.cisco.com/api/v1/networkdevice"
requests.get(wrongurl, headers=headers)

# Intent API documentation: https://developer.cisco.com/docs/dna-center