#!/bin/bash
config_file='/etc/apt/apt.conf.d/80certproxy'
#remove proxy settings from docker
if [[ "${1}" == "off" ]]; then
  echo "TURNING OFF PROXY FOR APT"
  sudo rm -rf "${config_file}"
  exit 0
fi

#populate proxy_ip and proxy_port variables
path=$(dirname $(readlink -f "${0}"))
. "${path}/get_proxy.sh"


echo -n "Username: "
read username
echo -n "Password: "
read -s password
encpassword=$(echo -n ${password}  | xxd -p | sed -e 's/\(..\)/%\1/g' )
echo 'Acquire::http::Proxy "http://'"${username}:${encpassword}@${proxy_ip}:${proxy_port}/"'";' | sudo tee "${config_file}"
echo 'Acquire::http::Timeout "360";' | sudo tee -a "${config_file}"
