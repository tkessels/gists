FROM debian:stretch
#FROM ubuntu:16.04

MAINTAINER tabledevil


RUN groupadd -g 999 user && \
    useradd -r -u 999 -g user user

USER user
