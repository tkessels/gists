#!/bin/bash


function restart_docker(){
  sudo systemctl daemon-reload
  sudo systemctl restart docker
  #systemctl show docker -p Environment
}

#remove proxy settings from docker
if [[ "${1}" == "off" ]]; then
  echo "TURNING OFF PROXY FOR DOCKER"
  sudo rm -v /etc/systemd/system/docker.service.d/http-proxy.conf
  restart_docker
  exit 0
fi

#populate proxy_ip and proxy_port variables
path=$(dirname $(readlink -f "${0}"))
. "${path}/get_proxy.sh"


echo -n "Username: "
read username
echo -n "Password: "
read -s password
#encpassword=$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "${password}")
#encpassword=$(echo -n ${password}  | sed -e 's/\@/\\x40/g' -e 's/\!/\\x21/g' -e 's/\$/\\x24/g' -e 's/\*/\\x2a/g' -e 's/\%/\\x25/g' -e 's/\&/\\x26/g' -e 's/\#/\\x30/g')
encpassword=$(echo -n ${password}  | xxd -p | sed -e 's/\(..\)/%%\1/g' )
echo "[Service]" | sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf >/dev/null
echo 'Environment="HTTP_PROXY=http://'"${username}"':"'"${encpassword}@${proxy_ip}:${proxy_port}/" | sudo tee -a /etc/systemd/system/docker.service.d/http-proxy.conf >/dev/null
echo 'Environment="HTTPS_PROXY=http://'"${username}"':"'"${encpassword}@${proxy_ip}:${proxy_port}/" | sudo tee -a /etc/systemd/system/docker.service.d/http-proxy.conf >/dev/null
echo -n '"NO_PROXY=localhost,127.0.0.1"' | sudo tee -a /etc/systemd/system/docker.service.d/http-proxy.conf >/dev/null

restart_docker
