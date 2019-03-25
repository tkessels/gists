FROM ubuntu:16.04
MAINTAINER tabledevil

USER root

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/jesparza/peepdf /opt/peepdf
RUN git clone https://github.com/DidierStevens/DidierStevensSuite /opt/didierstevenssuite

RUN apt-get update && apt-get install -y \
  python3-lxml \
  libemu2 \
  pkg-config \
  autoconf \
  pdftk \
  imagemagick \
  python-pil \
  python-pip \
  libboost-python-dev \
  libboost-thread-dev \
  libtool ; \
  rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/buffer/pyv8.git ; cd pyv8 ; python setup.py build && python setup.py install && cd .. && rm -rf pyv8
RUN git clone https://github.com/buffer/libemu.git ; cd libemu ; autoreconf -v -i && ./configure --prefix=/opt/libemu && make install && cd .. && rm -rf libemu2
RUN pip install pylibemu

RUN apt-get update && apt-get install -y exiftool ; rm -rf /var/lib/apt/lists/*

RUN chmod +x /opt/didierstevenssuite/*py
RUN ln -s /opt/peepdf/peepdf.py /bin/peepdf.py
RUN chmod +x /bin/peepdf.py
RUN chmod 777 -R /opt/peepdf/
RUN sed -i '/PDF/s/"none"/"read|write"/' /etc/ImageMagick-6/policy.xml

ENV PATH="/opt/didierstevenssuite/:${PATH}"
ADD README /opt/README
ADD command_help /opt/command_help
RUN echo 'cat /opt/README' >> /etc/bash.bashrc

RUN groupadd -g 1000 -r user && \
useradd -u 1000 -r -g user -d /home/user -s /sbin/nologin -c "Nonroot User" user && \
mkdir /home/user && \
chown -R user:user /home/user

RUN groupadd -g 1001 -r nonroot && \
useradd -u 1001 -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
mkdir /home/nonroot && \
chown -R nonroot:nonroot /home/nonroot

RUN pip install olefile

WORKDIR /home/nonroot/
USER nonroot
WORKDIR /home/nonroot/
CMD /bin/bash
