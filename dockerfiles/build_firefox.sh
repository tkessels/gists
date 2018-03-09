#!/bin/bash
docker build -f firefox.dockerfile . -t firefox
docker run -d --rm -p 5900:5900 --name firefox_vnc -e HOME=/ firefox x11vnc -forever -create
sleep 5
vncviewer localhost
docker stop firefox_vnc


