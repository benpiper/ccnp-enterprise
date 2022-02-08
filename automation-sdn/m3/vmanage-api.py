import json
import requests
from requests.auth import HTTPBasicAuth

# The vManage controller uses cookies for authentication

s = requests.Session()
data =  {
            'j_username':  'admin',
            'j_password':  'C1sco12345'
        }
headers = {'Content-type': 'application/x-www-form-urlencoded'}
url = "https://10.10.20.90:8443/j_security_check"
response = s.post(url, headers=headers, data=data, verify=False)

# To avoid TLS errors, add a DNS or hosts record for "vmanage"
# and use the URL https://vmanage:8443/j_security_check

# Use the vManage API to view devices

url = "https://10.10.20.90:8443/dataservice/device"
response = s.get(url, data=data, verify=False)

print(json.dumps(response.json(), indent=2))

url = "https://10.10.20.90:8443/dataservice/device/omp/routes/received?deviceId=10.10.1.13"
response = s.get(url, data=data, verify=False)

# The response has extraneous output, so we show only the "data" heading.

print(json.dumps(response.json()["data"], indent=2))

# SD-WAN API documentation: https://developer.cisco.com/docs/sdwan/