#!/bin/sh
# Stolen from Hippie2000 and modified by Jackfritt ;)
# Stolen from Jackfritt and modified by Chaosmaster :-P
ipddr="fritz.box"
unset dumpfile
unset passwd
if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ ! $1 ]; then
	echo "Usage: $0 <PASSWORD> [<DUMPFILE>] [<IP>]"
	exit 1
fi

[ $1 ] && passwd=$1
[ $2 ] && dumpfile="-w $2"
[ $3 ] && ipaddr=$3

# Challenge abholen
ChallengeXML=`wget -O - "http://$ipddr/cgi-bin/webcm?getpage=../html/login_sid.xml" 2>/dev/null| grep Challenge`
Challenge=`echo $ChallengeXML | awk '{match($0,/>[^<>]+</); print substr($0,RSTART+1,RLENGTH-2)}'`

# login aufbauen und hashen
CPSTR="$Challenge-$passwd"
MD5=`echo -n $CPSTR | iconv -f ISO8859-1 -t UTF-16LE | md5sum -b | awk '{print substr($0,1,32)}'`
RESPONSE="$Challenge-$MD5"
POSTDATA="login:command/response=$RESPONSE&getpage=../html/de/menus/menu2.html"

# login senden und SID herausfischen
SID=`wget -O - --post-data="$POSTDATA" "http://$ipddr/cgi-bin/webcm" 2>/dev/null| grep "name=\"sid\"" | head -1 | awk '{match($0,/value="[^"]+"/); print substr($0,RSTART+7,RLENGTH-8)}'`

# Internet Capture
wget -O - "http://$ipddr/cgi-bin/capture_notimeout?ifaceorminor=3-17 \
&snaplen=1600&capture=Start&sid=$SID" 2>/dev/null | \
wireshark -k $dumpfile -i -
