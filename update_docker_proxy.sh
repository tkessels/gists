#!/bin/bash
echo -n "Username: "
read username
echo -n "Password: "
read -s password
echo "[Service]" > /etc/systemd/system/docker.service.d/http-proxy.conf
echo -n "Environment=HTTPS_PROXY='http://" >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo -n "${username}:${password}@192.168.193.6:8080/' " >> /etc/systemd/system/docker.service.d/http-proxy.conf
echo -n '"NO_PROXY=localhost,127.0.0.1"'  >> /etc/systemd/system/docker.service.d/http-proxy.conf
systemctl daemon-reload
systemctl restart docker
