FROM ubuntu:16.04
MAINTAINER Tabledevil

RUN apt update && apt install -y locales
RUN locale-gen "en_US.UTF-8"
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN groupadd -g 1001 user && \
useradd -r -u 1001 -g user user

RUN apt update && apt install -y software-properties-common
RUN add-apt-repository -y ppa:gift/stable
RUN apt update && apt install -y python-plaso plaso-tools python-lzma python-pip
RUN pip install --upgrade lz4


USER user
WORKDIR /data
ENTRYPOINT ["/bin/bash"]
