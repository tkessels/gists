FROM ubuntu:xenial
LABEL maintainer="d4n6"
WORKDIR /data
RUN apt update && apt upgrade -y
RUN apt install python-pip -y
RUN pip install pip --upgrade
RUN pip install bencode artifacts pyelasticsearch
RUN apt install plaso -y
ENTRYPOINT ["/bin/bash"]

