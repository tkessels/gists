FROM ubuntu:16.04
MAINTAINER Tabledevil

RUN apt update && apt install -y locales
RUN locale-gen "en_US.UTF-8"
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN groupadd -g 1001 user && \
useradd -r -u 1001 -g user user

RUN apt update && apt install -y git cpanminus make

RUN git clone https://github.com/keydet89/RegRipper2.8
RUN mkdir /usr/local/lib/rip-lib
RUN cpanm -l /usr/local/lib/rip-lib Parse::Win32Registry
RUN cp /RegRipper2.8/rip.pl /usr/local/bin/rip
RUN chmod +x /usr/local/bin/rip
# RUN ln -s /RegRipper2.8/plugins /usr/local/bin/plugins
RUN sed -i '64s|"plugins"|"/RegRipper2.8/plugins"|' /usr/local/bin/rip
RUN sed -i "1i #!`which perl`" /usr/local/bin/rip
RUN sed -i '2i use lib qw(/usr/local/lib/rip-lib/lib/perl5/);' /usr/local/bin/rip
USER user
WORKDIR /data
ENTRYPOINT ["/bin/bash"]
