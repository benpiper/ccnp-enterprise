# Import the Python libraries we'll need to use the Intent API
import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth

# Using the username "devnetuser" and the password "Cisco123!"
# authenticate to DNAC to obtain a token that we'll use in future API requests

response = requests.post("https://sandboxdnac.cisco.com/api/system/v1/auth/token", \
    auth=HTTPBasicAuth("devnetuser","Cisco123!"))

# The response code is HTTP 200 OK, which means that the request was successful
response

# View the response in JSON format
response.json()

# The format of JSON is that of a key and value pair. "Token" is the key and
# the long random string that follows it is the value.

# Extract the token value and store it in the variable "token"
token = response.json()["Token"]
# To authenticate to the API, we need to pass in the token value using the
# x-auth-token HTTP header. We'll # structure this in JSON format.
headers = {
              'x-auth-token': response.json()["Token"]
          }

# We'll use the network-device API to obtain information on network devices in Cisco DNAC
url="https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"

# Send a GET request
response = requests.get(url, headers=headers)

# The response body is in JSON and it's long, making it difficult to read.
# We'll clean it up a bit using the json.dumps function.
print(json.dumps(response.json(), indent=2))

# We can get detailed information on a device by its IP address
url="https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/ip-address/10.10.20.80"
response = requests.get(url, headers=headers)
print(json.dumps(response.json(), indent=2))

# HTTP Response codes
# An HTTP response code that begins with 2xx is what you want, but it's not always what you get.
# If we had used invalid credentials when authenticating, we would have instead
# gotten an HTTP 401 Not Authenticated error
response401 = requests.post("https://sandboxdnac.cisco.com/api/system/v1/auth/token", \
    auth=HTTPBasicAuth("devnetuser","wrongpassword"))

# The response text gives us another clue
response401.text

# You'll also get a 401 response if you try to call the API without specifying a valid token.
# Notice we're leaving out the headers that contain the authentication token
requests.get(url)

# If you accidentally call a non-existent API, we'll get an HTTP 404 Not Found error
wrongurl="https://sandboxdnac.cisco.com/api/v1/networkdevices"
requests.get(wrongurl, headers=headers)

# Documentation for the Intent API is at https://developer.cisco.com/docs/dna-center/api/1-3-3-x/