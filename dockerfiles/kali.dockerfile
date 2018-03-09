FROM kalilinux/kali-linux-docker 
RUN apt update && \
    apt install -y nmap \
                mc \
                neofetch \
    && \
    rm -rf /var/cache/apt
CMD /bin/bash
