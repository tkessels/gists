#!/bin/bash
proxy_ip="192.168.x.x"
proxy_port="8080"

echo -n "Username: "
read username
echo -n "Password: "
read -s password
user=$(logname)
bashrc_file=/home/${user}/.bashrc
proxy_file=/home/${user}/.http_proxy

encpassword=$(echo -n ${password}  | xxd -p | sed -e 's/\(..\)/%\1/g' )

if ! grep -qF -e "PROXY_A93JK2" "${bashrc_file}" ; then
  echo "[ -f ${proxy_file} ] && . ${proxy_file} #PROXY_A93JK2" >> "${bashrc_file}"
fi

echo 'export "HTTP_PROXY=http://'"${username}"':"'"${encpassword}@${proxy_ip}:${proxy_port}/"  > "${proxy_file}"
echo 'export "HTTPS_PROXY=http://'"${username}"':"'"${encpassword}@${proxy_ip}:${proxy_port}/"  >> "${proxy_file}"
echo 'export "http_proxy=http://'"${username}"':"'"${encpassword}@${proxy_ip}:${proxy_port}/"  >> "${proxy_file}"
echo 'export "https_proxy=http://'"${username}"':"'"${encpassword}@${proxy_ip}:${proxy_port}/"  >> "${proxy_file}"
echo 'export "NO_PROXY=localhost,127.0.0.1"' >> "${proxy_file}"
