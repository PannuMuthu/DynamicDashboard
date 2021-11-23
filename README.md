# DynamicDashboard
Custom Scripts for Dynamic End-To-End Flow-Specific Grafana Dashboards

This repository serves as the codebase for a custom script to dynamically generate Grafana dashboards providing end-to-end flow-specific information provided a config file of relevant information.
The custom script has the following functionalities:
- Modifying the layout of the Grafana dashboard dynamically for multiple network elements
- Displaying flow-specific end-to-end information based on the config file information
- Dynamically constructing an SNMP Exporter config file to poll fine-grained OIDs from specific interfaces as specified in the config file
- Automatically turning on/off SNMP Exporter for specific scrape times and durations specified in config file through the SNMP Config File
- Automatically loading JSON files to Grafana via Dashboard HTTP API
- Dynamically generating Prometheus, Grafana, Pushgateway, Node Exporter, and SNMP Exporter Docker containers from base images within the script

## Python Script
The script that performs the dynamic dashboard generation is ```dynamic.py```. The python script takes in one argument via the command line of a config file containing the necessary details for dashboard generation. 

**Usage:** ```python dynamic.py <config_file>```

The output of the Python script is two files: 
- The Grafana Dashboard in JSON format (the script automatically also loads this into the Grafana server, but we provide the raw JSON as well): ```out.json```
- The Custom SNMP Config File which polls only the specific OIDs of the specific interfaces of the network elements described in the config file (as of now, must be manually loaded into the SNMP Exporter systemd service): ```snmp.yml```


## Config File
In this repository, there are multiple sample config files (```bottomFlowConfig.yml```, ```multiRandom.yml```, ```multiSwitchConfig.yml```, ```randomConfig.yml```, ```threeSwitchConfig.yml```, ```topFlowConfig.yml```, ```threeRandom.yml```). 
The config files contain the following information: 
- Host Information:
  - Host IP Address
  - Host Interface Name & IP
  - Host VLAN
  - Host Node Exporter Port
  - Corresponding Switch Interface Name & IP
- Network Element Information
  - Number of Network Elements
  - SNMP Exporter Job Name
  - Network Element IP Address
  - Network Element Interface In/Out Name & IP
  - Network Element SNMP Exporter OIDs

## Supporting Files
In order for the Python script to run, it utilizes a set of templating files as supporting files. Ensure that the following files are within the same directory of ```dynamic.py``` when running the script:
  - ```generator.yml```
  - ```generatorTemplate.yml```
  - ```template.json```
  - ```template2.json```
  - ```template3.json```
  - ```api.py```

***GRAFANA_API_KEY*** is a placeholder variable that should be replaced with your Grafana API authentication token. 
***SNMP_COMMUNITY_STRING*** is a placeholder variable that should be replaced with your network element's community read string.

## Installation

**Step 1:**
Download this repository in a directory with root access (preferrably within the root directory):
```git clone https://github.com/PannuMuthu/DynamicDashboard```

**Step 2: ** Configure Grafana as a Docker container.
