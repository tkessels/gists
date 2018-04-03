FROM ubuntu:xenial
LABEL maintainer="d4n6"
WORKDIR /data
COPY vol /usr/local/bin/volatility
RUN chmod +x /usr/local/bin/volatility
ENTRYPOINT ["/bin/bash"]
