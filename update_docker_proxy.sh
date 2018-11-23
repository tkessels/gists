#!/bin/bash
echo -n "Username: "
read username
echo -n "Password: "
read -s password
#encpassword=$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "${password}")
#encpassword=$(echo -n ${password}  | sed -e 's/\@/\\x40/g' -e 's/\!/\\x21/g' -e 's/\$/\\x24/g' -e 's/\*/\\x2a/g' -e 's/\%/\\x25/g' -e 's/\&/\\x26/g' -e 's/\#/\\x30/g')
encpassword=$(echo -n ${password}  | xxd -p | sed -e 's/\(..\)/%%\1/g' )
echo "[Service]" > /etc/systemd/system/docker.service.d/http-proxy.conf
echo 'Environment="HTTP_PROXY=http://'"${username}"':"'"${encpassword}"'"@192.168.193.6:8080/" ' >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo 'Environment="HTTPS_PROXY=http://'"${username}"':"'"${encpassword}"'"@192.168.193.6:8080/" ' >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo -n '"NO_PROXY=localhost,127.0.0.1"'  >> /etc/systemd/system/docker.service.d/http-proxy.conf
systemctl daemon-reload
systemctl restart docker
systemctl show docker -p Environment
