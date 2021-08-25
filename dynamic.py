#!/usr/bin/env python3

import yaml
import sys
import fileinput
import subprocess
import os
from datetime import datetime

# Help Command
if len(sys.argv) <= 1 or str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "-H":
        print("\n USAGE: python3 dynamic.py <config-file> \n \n Tip: Ensure that the Python script dynamic.py, the supporting files, and the config file are in one directory without subdirectories or other hierarchies.\n")
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
                print("\n USAGE: python3 dynamic.py <config-file> \n \n Tip: Ensure that the Python script dynamic.py, the supporting files, and the config file are in one directory without subdirectories or other hierarchies.\n")
        print("Parsing config file...")
        if data['switchNum'] == 1:
            print("Single Network Element Flow Detected")
            print("Collecting dashboard template...")
            with open('generatorTemplate.yml') as inGen, open('generator.yml', 'w') as outGen:
                 for line in inGen:
                     outGen.write(line)
            print("Reading SNMP OIDs/Interfaces/Scrape Duration/Scrape Time from config file...")
            oids = set(data['switchData']['params'])
            for i in range(len(oids)):
                oid = next(iter(oids))
                snip = "      - " + str(oid) + "\n"
                with open('generator.yml', 'r') as gen:
                    text = gen.readlines()
                text[3+i] = snip
                with open('generator.yml', 'w') as genOut:
                    genOut.writelines(text)
                oids.remove(oid)
            print("Writing SNMP Exporter generator config file...")
            subprocess.run("sudo mv generator.yml /root/go/src/github.com/prometheus/snmp_exporter/generator", shell=True)
            os.chdir('/root/go/src/github.com/prometheus/snmp_exporter/generator')
            print("Generating dynamic SNMP config file...")
            subprocess.run("./generator generate", shell=True)
            subprocess.run("sudo cp snmp.yml /root/DynamicDashboard", shell=True)
            os.chdir('/root/DynamicDashboard')
            print("Restarting SNMP Exporter instance with custom SNMP config file...")
            # Map of replacements to complete from template.json to out.json
            replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                            'IPHOSTB': str(data['hostB']['IP']),
                            'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                            'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                            'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                            'NAMEIFSWITCHA': str(data['hostA']['switchPort']['ifName']),
                            'NAMEIFSWITCHB': str(data['hostB']['switchPort']['ifName']),
                            'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                            'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                            'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                            'NODENAMEA': str(data['hostA']['nodeName']),
                            'NODENAMEB': str(data['hostB']['nodeName']),
                            'PORTA': str(data['hostA']['nodeExporterPort']),
                            'PORTB': str(data['hostB']['nodeExporterPort']),
                            'IPSWITCH': str(data['switchData']['target']),
                            'SNMPNAME': str(data['switchData']['job_name']),
                            'DASHTITLE': str(data['dashTitle']) + timeTxt }
            print("Creating custom Grafana JSON Dashboard...")

            # Iteratively find and replace in one go 
            with open('newTemplate.json') as infile, open('out.json', 'w') as outfile:
                for line in infile:
                    for src, target in replacements.items():
                        line = line.replace(src, target)
                    outfile.write(line)
            subprocess.run("sudo cp out.json /home/pmuthukumar", shell=True)

            print("Applying dashboard JSON to Grafana API...")
            # Run the API script to convert output JSON to Grafana dashboard automatically
            print("Loading Grafana dashboard on Grafana server...")
            subprocess.run("sudo python3 api.py out.json", shell=True)
            print("Loaded Grafana dashboard")
        else:
            print("Multiple Network Element Flow Detected")
            print("Collecting dashboard template...")
            with open('generatorTemplate.yml') as inGen, open('generator.yml', 'w') as outGen:
                 for line in inGen:
                     outGen.write(line)
            print("Reading SNMP OIDs/Interfaces/Scrape Duration/Scrape Time from config file...")
            oids = set()
            oids.update(data['switchDataA']['params'])
            oids.update(data['switchDataB']['params'])
            if data['switchNum'] == 3:
                oids.update(data['switchDataC']['params'])
            for i in range(len(oids)):
                oid = next(iter(oids))
                snip = "      - " + str(oid) + "\n"
                with open('generator.yml', 'r') as gen:
                    text = gen.readlines()
                text[3+i] = snip
                with open('generator.yml', 'w') as genOut:
                    genOut.writelines(text)
                oids.remove(oid)
            print("Writing SNMP Exporter generator config file...")
            subprocess.run("sudo mv generator.yml /root/go/src/github.com/prometheus/snmp_exporter/generator", shell=True)
            os.chdir('/root/go/src/github.com/prometheus/snmp_exporter/generator')
            print("Generating dynamic SNMP config file...")
            subprocess.run("./generator generate", shell=True)
            subprocess.run("sudo cp snmp.yml /root/DynamicDashboard", shell=True)
            os.chdir('/root/DynamicDashboard')
            print("Restarting SNMP Exporter instance with custom SNMP config file...")
            # Map of replacements to complete from template.json to out.json
            replacements = {}
            if data['switchNum'] == 2:
                replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                                'IPHOSTB': str(data['hostB']['IP']),
                                'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                                'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                                'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                                'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                                'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                                'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                                'NAMEIFAIN': str(data['hostA']['switchPort']['ifName']),
                                'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                                'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                                'NAMEIFBOUT': str(data['hostB']['switchPort']['ifName']),
                                'PORTA': str(data['hostA']['nodeExporterPort']),
                                'PORTB': str(data['hostB']['nodeExporterPort']),
                                'IPSWITCHA': str(data['switchDataA']['target']),
                                'IPSWITCHB': str(data['switchDataB']['target']),
                                'SNMPNAME': str(data['switchDataA']['job_name']),
                                'DASHTITLE':str(data['dashTitle']) + timeTxt}
            else:
                replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                                'IPHOSTB': str(data['hostB']['IP']),
                                'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                                'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                                'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                                'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                                'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                                'SWITCHBOUTGOING': str(data['switchDataB']['portOut']['ifIndex']),
                                'SWITCHCINCOMING': str(data['switchDataC']['portIn']['ifIndex']),
                                'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                                'NAMEIFAIN': str(data['switchDataA']['portIn']['ifName']),
                                'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                                'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                                'NAMEIFBOUT': str(data['switchDataB']['portOut']['ifName']),
                                'NAMEIFCIN': str(data['switchDataC']['portIn']['ifName']),
                                'NAMEIFCOUT': str(data['switchDataC']['portOut']['ifName']),
                                'PORTA': str(data['hostA']['nodeExporterPort']),
                                'PORTB': str(data['hostB']['nodeExporterPort']),
                                'IPSWITCHA': str(data['switchDataA']['target']),
                                'IPSWITCHB': str(data['switchDataB']['target']),
                                'IPSWITCHC': str(data['switchDataC']['target']),
                                'SNMPNAME': str(data['switchDataA']['job_name']),
                                'DASHTITLE':str(data['dashTitle']) + timeTxt}
            print("Creating custom Grafana JSON Dashboard...")

            # Iteratively find and replace in one go 
            fname = "template" + str(data['switchNum']) + ".json"
            with open(fname) as infile, open('out.json', 'w') as outfile:
                for line in infile:
                    for src, target in replacements.items():
                        line = line.replace(src, target)
                    outfile.write(line)
            subprocess.run("sudo cp out.json /home/pmuthukumar", shell=True)
            
            print("Applying dashboard JSON to Grafana API...")
            # Run the API script to convert output JSON to Grafana dashboard automatically
            print("Loading Grafana dashboard on Grafana server...")
            subprocess.run("sudo python3 api.py out.json", shell=True)
            print("Loaded Grafana dashboard")
    except KeyboardInterrupt:
        print("Interrupt detected")
        print("Shutting down SNMP Exporter instance to save resources...")

