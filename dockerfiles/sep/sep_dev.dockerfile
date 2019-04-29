FROM tabledevil/sep:base

LABEL maintainer="tabledevil"
LABEL docker.cmd="docker run -it --rm -v /mnt/sdc1:/data sep"

ADD start.sh /root/start.sh
RUN chmod +x /root/start.sh
ENTRYPOINT ["/root/start.sh"]
CMD ["shell"]
#RUN wget ftp://ftp.symantec.com/AVDEFS/symantec_antivirus_corp/static/symcdefs-core15unix.sh && chmod +x symcdefs-core15unix.sh && ./symcdefs-core15unix.sh && rm ./symcdefs-core15unix.sh
RUN service rtvscand start ; sleep 10 ; sav liveupdate -u ; sleep 10 ; while ! (sav info -d | grep -Pq '^\d') ; do sleep 1 ; done ; sav info -d | tee /root/tag ; service rtvscand stop ; sleep 10
