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

### Output Files 
 - ```out.json```

The Grafana Dashboard Script uses one of the dashboard templates (```template.json```, ```template2.json```, ```template3.json```, or ```template4.json```) based on the number of network elements defined in the config file to generate a JSON file of the Grafana Dashboard. The script then fills in the user-defined information of the flow using the config file parameters to create a JSON Grafana dashboard (```out.json```) file. The script then uses the Grafana API to automatically load the JSON dashboard to the specified running Grafana server. 

### Python Script Usage
Both of the scripts that perform the SNMP update and dynamic dashboard generation take in one argument via the command line of a config file containing the necessary details for dashboard generation. 

**Usage:** 
- ```python3 snmpUpdate.py <config_file>```
- ```python3 grafanaDashboard.py <config_file>```

The help option can provide additional guidance on running either script (```python3 snmpUpdate.py -h``` or ```python3 grafanaDashboard.py -h```). 
## Config File
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



