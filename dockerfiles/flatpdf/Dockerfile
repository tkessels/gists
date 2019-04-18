#FROM debian:stretch
#FROM ubuntu:16.04
FROM alpine
MAINTAINER tabledevil

RUN adduser -D -u 1000 user user

RUN apk add -u pdftk

USER user

ENTRYPOINT [ "pdftk","-","cat","output","-" ]
