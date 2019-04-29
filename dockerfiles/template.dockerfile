FROM debian:stretch
#FROM ubuntu:16.04

MAINTAINER tabledevil

#RUN apt-get update && apt-get install -y exiftool ; rm -rf /var/lib/apt/lists/*

RUN groupadd -g 999 user && \
    useradd -r -u 999 -g user user

USER user
