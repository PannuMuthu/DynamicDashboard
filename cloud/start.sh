#! /bin/bash

echo "!!    Make sure Port 3000, 9090, 9091, 9469 are not in use"
echo "!!    sudo lsof -i -P -n | grep LISTEN"
echo "!!    Check Port 3000"
sudo lsof -i -P -n | grep 3000
echo "!!    Check Port 9090"
sudo lsof -i -P -n | grep 9090
echo "!!    Check Port 9091"
sudo lsof -i -P -n | grep 9091
echo "!!    Check Port 9469"
sudo lsof -i -P -n | grep 9469

echo "!!    Remove previous stack"
docker stack rm could
echo "!!    Previous stack revmoed"

echo "!!    Start Grafana-server"
sudo systemctl start grafana-server

echo "!!    Deploy promethues and pushgateway"
docker stack deploy -c docker-stack.yml cloud

echo "!!    Deploy script exporter"
yes | cp -rfa se_config/. script_exporter/examples

read -r -p "Generate Grafana Dashboar? [y/N enter]: " grafana
if [ "$grafana" == "y" ] || [ "$grafana" == "Y" ]; then
    cd ..
    cd PrometheusGrafana
    python3 dynamic.py
else 
    echo "Skip Grafana Dashboard Generation"
fi

# read -r -p "Start script exporter? [y/N]: " script

# if [ "$script" == "y" ] || [ "$script" == "Y" ]; then

# fi