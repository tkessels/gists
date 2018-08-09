FROM ubuntu:16.04
MAINTAINER tabledevil

USER root
RUN apt-get update && apt-get install -y \
  git \
  python3-lxml \
  libemu2 \
  pkg-config \
  autoconf \
  python-pil \
  python-pip ; \
  pip install pylibemu ; \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

RUN git clone https://github.com/jesparza/peepdf /opt/peepdf
RUN git clone https://github.com/DidierStevens/DidierStevensSuite /opt/DidierStevensSuite

USER root
WORKDIR /home/nonroot/

RUN ln -s /opt/peepdf/peepdf.py /bin/peepdf.py
RUN chmod +x /bin/peepdf.py


#USER nonroot
WORKDIR /home/nonroot/
CMD /bin/bash
