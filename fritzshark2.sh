#!/bin/sh
IP="fritz.box"
echo -n Password: 
read -s Passwd

# Challenge abholen
Challenge=`wget -O - "http://$IP/login_sid.lua" 2>/dev/null | sed 's/.*<Challenge>\(.*\)<\/Challenge>.*/\1/'`

# login aufbauen und hashen
CPSTR="$Challenge-$Passwd"
MD5=`echo -n $CPSTR | iconv -f ISO8859-1 -t UTF-16LE | md5sum -b | awk '{print substr($0,1,32)}'`
RESPONSE="$Challenge-$MD5"
POSTDATA="?username=&response=$RESPONSE"

# login senden und SID herausfischen
SID=`wget -O - --post-data="$POSTDATA" "http://$IP/login_sid.lua" 2>/dev/null | sed 's/.*<SID>\(.*\)<\/SID>.*/\1/'`

# Internet Capture
#Schnittstelle 1(Internet)=3-17
#wget -O - "http://$IP/cgi-bin/capture_notimeout?ifaceorminor=3-17 \
#alle Schnittstellen =3-0
#wget -O - "http://$IP/cgi-bin/capture_notimeout?ifaceorminor=3-0 \
#&snaplen=1600&capture=Start&sid=$SID" 2>/dev/null | \
#tshark -i - -S -l -N nmtC
#wget -O - "http://$IP/cgi-bin/capture_notimeout?ifaceorminor=3-0 \
#Externe Schnittstelle
#wget -O - "http://$IP/cgi-bin/capture_notimeout?ifaceorminor=3-17 \
#Lokal LAN
#wget -O - "http://$IP/cgi-bin/capture_notimeout?ifaceorminor=1-eth0&snaplen=1600&capture=Start&sid=$SID" 2>/dev/null | tshark -i - -S -l -N nmtC
wget -O - "http://$IP/cgi-bin/capture_notimeout?ifaceorminor=1-eth0&snaplen=1600&capture=Start&sid=$SID" 2>/dev/null | tcpdump -r - -w /tmp/trace -W 48 -G 1800 -C 100 -K -n
