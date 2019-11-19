#!/bin/bash

proxy_ip=$(env | grep http_proxy | grep -Pio '[^@/:]+(?=:\d+/?$)')
proxy_port=$(env | grep http_proxy | grep -Pio '(?<=:)(\d+)(?=/?$)')

if [ -z "${proxy_ip}" ]; then
  echo "Enter Proxy IP or Hostname (no port): "
  read proxy_ip
else
  echo "Using >>${proxy_ip}<< as Proxy-Address"
fi

if [ -z "${proxy_port}" ]; then
  echo -n "Proxy-Port: "
  read proxy_port
else
  echo "Using >>${proxy_port}<< as Proxy-Port"
fi

echo "Using ${proxy_ip}:${proxy_port} as Proxy!"

