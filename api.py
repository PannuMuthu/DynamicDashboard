import requests 
import json
import sys

server = "http://198.32.43.16:3000"
# Get Default Home Dashboard
url = server + "/api/dashboards/db"
headers = {"Authorization": "Bearer eyJrIjoia1Y2QXFjZU9CbW1yZ2dRUUFYYVdrR3JZRXVVcFBZcTAiLCJuIjoiYWRtaW4iLCJpZCI6MX0=",
            "Content-Type": "application/json",
            "Accept": "application/json"}
f = open(sys.argv[1],)
x = json.load(f)
r = requests.post(url=url, headers=headers, data=json.dumps(x), verify=False)
print(r.json())
