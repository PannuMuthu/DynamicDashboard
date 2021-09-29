#!/usr/bin/env python3

import requests 
import json
import sys

server = "http://198.32.43.16:3000"
# Get Default Home Dashboard
url = server + "/api/dashboards/db"
# HTTP Post Header
# Replace with your Grafana API key
headers = {"Authorization": GRAFANA_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"}
# Open and load out.json input
f = open(sys.argv[1],)
x = json.load(f)
# HTTP Post Request
r = requests.post(url=url, headers=headers, data=json.dumps(x), verify=False)
print(r.json())
