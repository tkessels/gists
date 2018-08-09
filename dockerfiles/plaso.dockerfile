FROM ubuntu:16.04

MAINTAINER tabledevil


RUN groupadd -g 999 user && \
    useradd -r -u 999 -g user user

RUN echo "deb http://ppa.launchpad.net/gift/dev/ubuntu xenial main" > /etc/apt/sources.list.d/gift.list
RUN echo "deb-src http://ppa.launchpad.net/gift/dev/ubuntu xenial main" >> /etc/apt/sources.list.d/gift.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 10C598B8

RUN apt update && apt install -y \
    python-plaso \
    plaso-tools \
    python-elasticsearch \
    && rm -rf /var/lib/apt/lists/*

USER user
