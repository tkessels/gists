FROM ubuntu:16.04

LABEL maintainer="tabledevil"
LABEL docker.cmd="docker run -it --rm -v /mnt/sdc1:/data sep"

RUN apt-get update && apt-get install -y wget default-jre lib32ncurses5 lib32z1 sharutils ; rm -rf /var/lib/apt/lists/*
ADD sep.tar.gz /root/
WORKDIR /root
RUN chmod +x /root/sep/install.sh
RUN /root/sep/install.sh -i && rm -rf /root/sep
RUN ln -s /opt/Symantec/symantec_antivirus/sav /usr/local/bin/sav
WORKDIR /data
