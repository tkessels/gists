FROM alpine

MAINTAINER tabledevil
RUN echo -e "none\nnone\n" | adduser user -u 1001
RUN mkdir /data

RUN apk add -u git python python3 py-olefile

RUN git clone https://github.com/DidierStevens/DidierStevensSuite /opt/DidierStevensSuite
RUN chmod +x /opt/DidierStevensSuite/*
ENV PATH="/opt/DidierStevensSuite/:${PATH}"



WORKDIR /data
# USER user
