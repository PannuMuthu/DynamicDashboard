# DynamicDashboard
Custom Scripts for Dynamic End-To-End Flow-Specific Grafana Dashboards

This repository serves as the codebase for a set of custom scripts to dynamically generate Grafana dashboards providing end-to-end flow-specific information provided a config file of relevant information.
This branch provides two Python scripts (```snmpUpdate.py``` and ```grafanaDashboard.py```). 

## SNMP Update Script (```snmpUpdate.py```)

```snmpUpdate.py``` fine-tunes the SNMP Exporter polling a network element by configuring the SNMP Exporter to poll a set of user-defined OIDs for a set of user-defined interfaces in the network element with a user-defined scrape duration and scrape interval, specified in the config file (either ```NERSC_SNMP_CONFIG.yml``` or ```SLAC_SNMP_CONFIG.yml```). 

### Required Supporting Files
 - ```generatorTemplate.yml```
 - ```NERSC_SNMP_CONFIG.yml``` or ```SLAC_SNMP_CONFIG.yml```

### Output Files 
 - ```generator.yml```
 - ```snmp.yml```

The SNMP Update script leverages the functionality from the SNMP Exporter Generator, which creates custom SNMP Exporter config files based on a Generator config file where we can specify the scrape duration, OIDs, community read string, etc. The script uses the ```generatorTemplate.yml``` file to create a Generator config file using the user-defined config file parameters. Using a set of bash commands run within the script, the script feeds the custom Generator config file into the SNMP Exporter Generator, which generates a custom SNMP Exporter config file. The script then reloads the SNMP Exporter systemd service with the updated SNMP Exporter config file so that the new SNMP Exporter is a fine-grained light-weight SNMP Exporter polling only the OIDs/Interfaces/Scrape Time/Scrape Duration of the data flow as specified in the user-defined config file. 

## Grafana Dashboard Script (```grafanaDashboard.py```)

```grafana Dashboard.py``` dynamically creates a Grafana dashboard visualizing various aspects of the end-to-end data flow using parameters from the user-defined config file description of the flow (```GRAFANA_CONFIG.yml```). 

### Required Supporting Files
 - ```template.json```, ```template2.json```, ```template3.json```, ```template4.json```
 - ```GRAFANA_CONFIG.yml```
 - ```api.py```

### Output Files 
 - ```generator.yml```
 - ```snmp.yml```

The Grafana Dashboard Script uses one of the dashboard templates (```template.json```, ```template2.json```, ```template3.json```, or ```template4.json```) based on the number of network elements defined in the config file to generate a JSON file of the Grafana Dashboard. 

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


