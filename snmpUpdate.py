#!/usr/bin/env python3

import yaml
import sys
import fileinput
import subprocess
import os
from datetime import datetime

# Help Command
if len(sys.argv) <= 1 or str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "-H":
        print("\n USAGE: python3 snmpUpdate.py <config-file> \n \n Tip: Ensure that the Python script snmpUpdate.py, the supporting files, and the config file are in one directory without subdirectories or other hierarchies.\n")
else: 
    try:
        print("Starting script...")
        # Load yaml config file as dict
        print("Parsing config file...")
        data = {}
        with open(sys.argv[1], 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("\n USAGE: python3 snmpUpdate.py <config-file> \n \n Tip: Ensure that the Python script snmpUpdate.py, the supporting files, and the config file are in one directory without subdirectories or other hierarchies.\n")
        with open('generatorTemplate.yml') as inGen, open('generator.yml', 'w') as outGen:
             for line in inGen:
                 outGen.write(line)
        print("Reading SNMP OIDs/Interfaces/Scrape Duration/Scrape Time from config file...")
        oids = set(data['switchData']['params'])
        with open('generator.yml', 'r') as gen:
            text = gen.readlines()
        text[6] = "    timeout: " + str(data['switchData']['timeOutDuration']) + "\n"
        text[10] = "      community: " + str(data['switchData']['communityString']) + "\n"
        for i in range(len(oids)):
            oid = next(iter(oids))
            snip = "      - " + str(oid) + "\n"
            text[3+i] = snip
            with open('generator.yml', 'w') as genOut:
                genOut.writelines(text)
            oids.remove(oid)
        print("Writing SNMP Exporter generator config file...")
        # Replace with the path to SNMP Exporter generator
        genPath = str(data['switchData']['snmpGeneratorPath'])
        snmpPath = str(data['switchData']['snmpExporterPath'])
        dashPath = str(data['switchData']['dynamicDashboardPath'])
        cmd1 = "sudo mv generator.yml " + genPath
        subprocess.run(cmd1, shell=True)
        os.chdir(genPath)
        print("Generating dynamic SNMP config file...")
        subprocess.run("./generator generate", shell=True)
        # Replace with path to Dynamic Dashboard directory location
        cmd2 = "sudo cp snmp.yml " + dashPath
        subprocess.run(cmd2, shell=True)
        os.chdir(dashPath)
        print("Replacing SNMP Exporter config file...")
        cmd3 = "sudo mv snmp.yml " + snmpPath + "/snmp.yml"
        subprocess.run(cmd3, shell=True)
        print("Restarting SNMP Exporter instance with custom SNMP config file...")
        # Skip if SNMP Exporter is not configured as systemd service
        subprocess.run("sudo systemctl restart snmp-exporter", shell=True)
    except KeyboardInterrupt:
        print("Interrupt detected")
        print("Shutting down SNMP Exporter instance to save resources...")

