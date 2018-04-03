FROM ubuntu:xenial
LABEL maintainer="d4n6"
WORKDIR /data
RUN apt update && apt upgrade -y ; apt install software-properties-common python-software-properties -y
RUN add-apt-repository ppa:gift/stable -y ; apt update ; apt install python-plaso plaso-tools -y
ENTRYPOINT ["/bin/bash"]

