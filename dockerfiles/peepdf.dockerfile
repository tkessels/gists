FROM ubuntu:16.04
MAINTAINER tabledevil

USER root
RUN apt-get update && apt-get install -y \
  git \
  python3-lxml \
  python-libemu \
  libemu2 \
  libemu-dev \
  libboost-all-dev \
  python-pip ; \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

RUN git clone https://github.com/jesparza/peepdf /opt/peepdf

USER root
WORKDIR /home/nonroot/
#RUN pip install -v pyv8
RUN ln -s /opt/peepdf/peepdf.py /bin/peepdf.py
RUN chmod +x /bin/peepdf.py


#USER nonroot
WORKDIR /home/nonroot/
CMD /bin/bash
