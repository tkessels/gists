FROM alpine
MAINTAINER Tabledevil
RUN apk add --no-cache -u git
RUN git clone https://github.com/google/rekall.git /rekall
RUN apk add --no-cache -u python py2-pip python2-dev
RUN apk add --no-cache -u linux-headers
RUN apk add --no-cache -u build-base
RUN apk add --no-cache -u readline-dev
RUN pip install --upgrade setuptools pip wheel
RUN pip install --editable rekall/rekall-lib
RUN sed -i -e 's/PyYAML==4.1/PyYAML==3.13/' /rekall/rekall-core/setup.py
RUN pip install --editable rekall/rekall-core
RUN pip install --editable rekall/rekall-agent
RUN apk add --no-cache -u bash
RUN apk add --no-cache -u alpine-sdk
RUN apk add --no-cache -u ncurses-dev
RUN pip install future==0.16.0
RUN pip install --editable rekall
