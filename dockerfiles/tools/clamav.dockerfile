FROM alpine
ARG PUID=1001
ARG PGID=1001

MAINTAINER tabledevil

RUN apk add -u clamav
RUN apk add -u freshclam
RUN freshclam


RUN addgroup -g ${PGID} user && \
    adduser -D -u ${PUID} -G user user

USER user
