FROM kalilinux/kali-linux-docker
MAINTAINER Tabledevil
RUN apt-get update && apt-get install -y john ; rm -rf /var/lib/apt/lists/*
