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

## Configuration

**Step 1:**
Download this repository in a directory with root access (preferrably within the root directory):
- ```git clone https://github.com/PannuMuthu/DynamicDashboard```

**Step 2:** Configure Grafana as a Docker container. Since the dynamic dashboard script relies on the Grafana API, we must manually generate an API key to provide the script. For all other polling software (Prometheus, Pushgateway, Node Exporter, SNMP Exporter), the script will automatically generate the containers through the base image CLI commands.
- ```docker run -d   -p 3000:3000   -e "GF_INSTALL_PLUGINS=jdbranham-diagram-panel"   grafana/grafana```
Ensure the docker container is running and keep track of the container ID: 
- ```docker ps```
Now, through either an SSH tunnel or an alternative, navigate to ```http://localhost:3000``` and login to Grafana with the default authentication (username: admin, password: admin). Add Prometheus as a datasource (https://grafana.com/docs/grafana/v7.5/datasources/add-a-data-source/?utm_source=grafana_gettingstarted) by setting the URL to ```http://localhost:9090``` and the Access to ```Browser```. 
Finally, generate an API key by navigating to the API Keys tab within Grafana and generating a new API key with ```admin``` access and no expiration date. Save the API token value which starts with ```Bearer ...```. 

**Step 3: Configure Scripts**
Navigate to the ```api.py``` script within the DynamicDashboard directory and replace the ```GRAFANA_API_KEY``` placeholder with the Grafana API key saved in the previous step. Additionally, navigate to the ```generatorTemplate.yml``` file within the DynamicDashboard directory and replace the ```SNMP_COMMUNITY_STRING``` placeholder with the SNMP community read string. 

## Execution

Assuming the Dynamic Dashboard scripts have been configured, run the scripts by issuing the following command:
- ```python dynamic.py <config_file>```
where ```<config_file>``` is the user-generated config file detailing the configuration parameters of the flow we wish to visualize. Examples of sample config file formats are located within the ```Sample Configs``` directory. 
