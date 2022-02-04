import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth
# Authenticate to the vManage controller. It uses cookies for authentication, so we won't have to manually store and pass a token as before.
s = requests.Session()
data =  {
            'j_username':  "devnetuser",
            'j_password':  "RG!_Yw919_83"
        }
url = "https://sandbox-sdwan-1.cisco.com/j_security_check"
response = s.post(url, data=data, verify=False)
# Use the vManage API to view devices
url = "https://sandbox-sdwan-1.cisco.com/dataservice/device"
url = "https://sandbox-sdwan-1.cisco.com/dataservice/device/omp/routes/received?deviceId=10.10.1.3"

response = s.get(url, data=data, verify=False)
# The response contains column heading definitions, so to show only the interesting information, we'll restrict the output to the "data" object.
print(json.dumps(response.json()["data"], indent=2))