#!/usr/bin/env python3

import yaml
import requests 
import json
import sys
import fileinput
import subprocess
import os
from datetime import datetime

# Help Command
if len(sys.argv) <= 1 or str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "-H":
        print("\n USAGE: python3 grafanaDashboard.py <config-file> \n \n Tip: Ensure that the Python script grafanaDashboard.py, the supporting files, and the config file are in one directory without subdirectories or other hierarchies.\n")
else: 
    try:
        print("Starting script...")
        # Help Command
        # Get current time stamp
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y_%H:%M:%S")
        timeTxt = " ( " + str(current_time) + " )"
        # Load yaml config file as dict
        data = {}
        with open(sys.argv[1], 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("\n USAGE: python3 grafanaDashboard.py <config-file> \n \n Tip: Ensure that the Python script grafanaDashboard.py, the supporting files, and the config file are in one directory without subdirectories or other hierarchies.\n")
        print("Parsing config file...")
        if data['switchNum'] == 1:
            print("Single Network Element Flow Detected")
            print("Collecting dashboard template...")
            # Map of replacements to complete from template.json to out.json
            replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                            'IPHOSTB': str(data['hostB']['IP']),
                            'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                            'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                            'IFNAMESWITCHHOSTA': str(data['switchData']['portIn']['ifIndex']),
                            'NAMEIFSWITCHA': str(data['switchData']['portIn']['ifName']),
                            'NAMEIFSWITCHB': str(data['switchData']['portOut']['ifName']),
                            'IFNAMESWITCHHOSTB': str(data['switchData']['portOut']['ifIndex']),
                            'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                            'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                            'NODENAMEA': str(data['hostA']['nodeName']),
                            'NODENAMEB': str(data['hostB']['nodeName']),
                            'PORTA': str(data['hostA']['nodeExporterPort']),
                            'PORTB': str(data['hostB']['nodeExporterPort']),
                            'IPSWITCH': str(data['switchData']['target']),
                            'SNMPNAME': str(data['switchData']['job_name']),
                            'SWITCHNAME': str(data['switchData']['name']),
                            'DASHTITLE': str(data['dashTitle']) + timeTxt }
            print("Creating custom Grafana JSON Dashboard...")

            # Iteratively find and replace in one go 
            with open('newTemplate.json') as infile, open('out.json', 'w') as outfile:
                for line in infile:
                    for src, target in replacements.items():
                        line = line.replace(src, target)
                    outfile.write(line)

            print("Applying dashboard JSON to Grafana API...")
            # Run the API script to convert output JSON to Grafana dashboard automatically
            print("Loading Grafana dashboard on Grafana server...")
            # Change to Grafana Server location
            server = "http://198.32.43.16:3000"
            # Get Default Home Dashboard
            url = server + "/api/dashboards/db"
            # HTTP Post Header

            # Change to your Grafana API Key Value pair
            headers = {"Authorization": GRAFANA_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"}
            # Open and load out.json input
            f = open('out.json',)
            x = json.load(f)
            # HTTP Post Request
            r = requests.post(url=url, headers=headers, data=json.dumps(x), verify=False)
            print(r.json())
            print("Loaded Grafana dashboard")
        else:
            print("Multiple Network Element Flow Detected")
            print("Collecting dashboard template...")
            # Map of replacements to complete from template.json to out.json
            replacements = {}
            if data['switchNum'] == 2:
                replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                                'IPHOSTB': str(data['hostB']['IP']),
                                'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                                'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                                'IFNAMESWITCHHOSTA': str(data['switchDataA']['portIn']['ifIndex']),
                                'IFNAMESWITCHHOSTB': str(data['switchDataB']['portOut']['ifIndex']),
                                'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                                'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                                'NAMEIFAIN': str(data['hostA']['switchDataA']['portIn']['ifName']),
                                'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                                'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                                'NAMEIFBOUT': str(data['switchDataB']['portOut']['ifName']),
                                'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                                'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                                'NODENAMEA': str(data['hostA']['nodeName']),
                                'NODENAMEB': str(data['hostB']['nodeName']),
                                'PORTA': str(data['hostA']['nodeExporterPort']),
                                'PORTB': str(data['hostB']['nodeExporterPort']),
                                'IPSWITCHA': str(data['switchDataA']['target']),
                                'IPSWITCHB': str(data['switchDataB']['target']),
                                'SNMPNAME': str(data['switchDataA']['job_name']),
                                'SWITCHANAME': str(data['switchDataA']['name']),
                                'SWITCHBNAME': str(data['switchDataB']['name']),
                                'DASHTITLE':str(data['dashTitle']) + timeTxt}
            elif data['switchNum'] == 3:
                replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                                'IPHOSTB': str(data['hostB']['IP']),
                                'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                                'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                                'IFNAMESWITCHHOSTA': str(data['switchDataA']['portIn']['ifIndex']),
                                'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                                'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                                'SWITCHBOUTGOING': str(data['switchDataB']['portOut']['ifIndex']),
                                'SWITCHCINCOMING': str(data['switchDataC']['portIn']['ifIndex']),
                                'IFNAMESWITCHHOSTB': str(data['switchDataC']['portOut']['ifIndex']),
                                'NAMEIFAIN': str(data['switchDataA']['portIn']['ifName']),
                                'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                                'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                                'NAMEIFBOUT': str(data['switchDataB']['portOut']['ifName']),
                                'NAMEIFCIN': str(data['switchDataC']['portIn']['ifName']),
                                'NAMEIFCOUT': str(data['switchDataC']['portOut']['ifName']),
                                'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                                'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                                'NODENAMEA': str(data['hostA']['nodeName']),
                                'NODENAMEB': str(data['hostB']['nodeName']),
                                'PORTA': str(data['hostA']['nodeExporterPort']),
                                'PORTB': str(data['hostB']['nodeExporterPort']),
                                'IPSWITCHA': str(data['switchDataA']['target']),
                                'IPSWITCHB': str(data['switchDataB']['target']),
                                'IPSWITCHC': str(data['switchDataC']['target']),
                                'SNMPNAME': str(data['switchDataA']['job_name']),
                                'SWITCHANAME': str(data['switchDataA']['name']),
                                'SWITCHBNAME': str(data['switchDataB']['name']),
                                'SWITCHCNAME': str(data['switchDataC']['name']),
                                'DASHTITLE':str(data['dashTitle']) + timeTxt}
            else:
                replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                                'IPHOSTB': str(data['hostB']['IP']),
                                'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                                'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                                'IFNAMESWITCHHOSTA': str(data['switchDataA']['portIn']['ifIndex']),
                                'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                                'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                                'SWITCHBOUTGOING': str(data['switchDataB']['portOut']['ifIndex']),
                                'SWITCHCINCOMING': str(data['switchDataC']['portIn']['ifIndex']),
                                'SWITCHCOUTGOING': str(data['switchDataC']['portOut']['ifIndex']),
                                'SWITCHDINCOMING': str(data['switchDataD']['portIn']['ifIndex']),
                                'IFNAMESWITCHHOSTB': str(data['switchDataD']['portOut']['ifIndex']),
                                'NAMEIFAIN': str(data['switchDataA']['portIn']['ifName']),
                                'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                                'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                                'NAMEIFBOUT': str(data['switchDataB']['portOut']['ifName']),
                                'NAMEIFCIN': str(data['switchDataC']['portIn']['ifName']),
                                'NAMEIFCOUT': str(data['switchDataC']['portOut']['ifName']),
                                'NAMEIFDIN': str(data['switchDataD']['portIn']['ifName']),
                                'NAMEIFDOUT': str(data['switchDataD']['portOut']['ifName']),
                                'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                                'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                                'NODENAMEA': str(data['hostA']['nodeName']),
                                'NODENAMEB': str(data['hostB']['nodeName']),
                                'PORTA': str(data['hostA']['nodeExporterPort']),
                                'PORTB': str(data['hostB']['nodeExporterPort']),
                                'IPSWITCHA': str(data['switchDataA']['target']),
                                'IPSWITCHB': str(data['switchDataB']['target']),
                                'IPSWITCHC': str(data['switchDataC']['target']),
                                'IPSWITCHD': str(data['switchDataD']['target']),
                                'SNMPNAME': str(data['switchDataA']['job_name']),
                                'SWITCHANAME': str(data['switchDataA']['name']),
                                'SWITCHBNAME': str(data['switchDataB']['name']),
                                'SWITCHCNAME': str(data['switchDataC']['name']),
                                'SWITCHDNAME': str(data['switchDataD']['name']),
                                'DASHTITLE':str(data['dashTitle']) + timeTxt}
            print("Creating custom Grafana JSON Dashboard...")

            # Iteratively find and replace in one go 
            fname = "template" + str(data['switchNum']) + ".json"
            with open(fname) as infile, open('out.json', 'w') as outfile:
                for line in infile:
                    for src, target in replacements.items():
                        line = line.replace(src, target)
                    outfile.write(line)
            
            print("Applying dashboard JSON to Grafana API...")
            # Run the API script to convert output JSON to Grafana dashboard automatically
            print("Loading Grafana dashboard on Grafana server...")
            # Change to Grafana Server location
            server = "http://198.32.43.16:3000"
            # Get Default Home Dashboard
            url = server + "/api/dashboards/db"

            # Change to your Grafana API Key Value pair
            headers = {"Authorization": GRAFANA_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"}
            # Open and load out.json input
            f = open('out.json',)
            x = json.load(f)
            # HTTP Post Request
            r = requests.post(url=url, headers=headers, data=json.dumps(x), verify=False)
            print(r.json())
            print("Loaded Grafana dashboard")
    except KeyboardInterrupt:
        print("Interrupt detected")
        print("Shutting down SNMP Exporter instance to save resources...")
