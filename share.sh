#!/bin/bash
#ifconfig eth1 10.10.10.1/24
sysctl -w net.ipv4.conf.all.forwarding=1
iptables -t nat -F
iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE 

