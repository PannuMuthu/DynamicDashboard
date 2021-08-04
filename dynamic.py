#!/usr/bin/env python3

import yaml
import sys
import fileinput
import subprocess
import os

# Load yaml config file as dict
data = {}
with open(sys.argv[1], 'r') as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Single network element 
if data['switchNum'] == 1:
    # Dynamically create SNMP Config file based on OIDs listed in switchData params
    with open('generatorTemplate.yml') as inGen, open('generator.yml', 'w') as outGen:
         for line in inGen:
             outGen.write(line)
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
    # Run the SNMP Generator script and move to the DynamicDashboard directory
    subprocess.run("sudo mv generator.yml /root/go/src/github.com/prometheus/snmp_exporter/generator", shell=True)
    os.chdir('/root/go/src/github.com/prometheus/snmp_exporter/generator')
    subprocess.run("./generator generate", shell=True)
    subprocess.run("sudo cp snmp.yml /root/DynamicDashboard", shell=True)
    os.chdir('/root/DynamicDashboard')

    # Creating Grafana dashboard JSON dynamically
    # Map of replacements to complete from template.json to out.json
    replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                    'IPHOSTB': str(data['hostB']['IP']),
                    'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                    'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                    'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                    'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                    'PORTA': str(data['hostA']['nodeExporterPort']),
                    'PORTB': str(data['hostB']['nodeExporterPort']),
                    'IPSWITCH': str(data['switchData']['target']),
                    'SNMPNAME': str(data['switchData']['job_name'])}

    # Iteratively find and replace in one go 
    with open('template.json') as infile, open('out.json', 'w') as outfile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            outfile.write(line)
    subprocess.run("sudo cp out.json /home/pmuthukumar", shell=True)
# Multiple Network Elements
else:
    # Create SNMP Exporter config file dynamically
    with open('generatorTemplate.yml') as inGen, open('generator.yml', 'w') as outGen:
         for line in inGen:
             outGen.write(line)
    # Use unique OIDs from all switchData params for each network element
    oids = set()
    oids.update(data['switchDataA']['params'])
    oids.update(data['switchDataB']['params'])
    for i in range(len(oids)):
        oid = next(iter(oids))
        snip = "      - " + str(oid) + "\n"
        with open('generator.yml', 'r') as gen:
            text = gen.readlines()
        text[3+i] = snip
        with open('generator.yml', 'w') as genOut:
            genOut.writelines(text)
        oids.remove(oid)
    subprocess.run("sudo mv generator.yml /root/go/src/github.com/prometheus/snmp_exporter/generator", shell=True)
    os.chdir('/root/go/src/github.com/prometheus/snmp_exporter/generator')
    subprocess.run("./generator generate", shell=True)
    subprocess.run("sudo cp snmp.yml /root/DynamicDashboard", shell=True)
    os.chdir('/root/DynamicDashboard')

    # Creating Grafana dashboard JSON dynamically
    # Map of replacements to complete from template.json to out.json
    # Formatting works up to 4 network elements + 2 hosts, but becomes too crowded along horizontal axis
    # Theoretically, Grafana dashboards support up to 8 network elements + 2 hosts, but it will be extremely crowded
    replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                    'IPHOSTB': str(data['hostB']['IP']),
                    'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                    'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                    'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                    'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                    'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                    'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                    'PORTA': str(data['hostA']['nodeExporterPort']),
                    'PORTB': str(data['hostB']['nodeExporterPort']),
                    'IPSWITCHA': str(data['switchDataA']['target']),
                    'IPSWITCHB': str(data['switchDataB']['target']),
                    'SNMPNAME': str(data['switchDataA']['job_name'])}

    # Iteratively find and replace in one go 
    with open('templateTwo.json') as infile, open('out.json', 'w') as outfile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            outfile.write(line)
    subprocess.run("sudo cp out.json /home/pmuthukumar", shell=True)

