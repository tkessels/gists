#!/bin/bash

#disabling Kernellogging to Console
echo '2 4 1 7' > /proc/sys/kernel/printk

#rechnet die eine centrierierte fensterposition aus anhand von bildschirm- & fenstergröße 
# 'mitte 50'
function mitte(){
cols=$(tput cols)
mitte=$(echo $(( $cols / 2 - $1 / 2 )) )
echo $mitte
}

#zeigt eine infomeldung für x-Sekunden an
# 'info text 5'
function info(){
	text=${1}
	text_len=$(( ${#1} + 4 ))
	timeout=${2}
	dialog	--backtitle "CERTBw - Zero-Wipe" --infobox "$text" 3 $text_len; sleep $timeout
}

#zeigt überischt von datenträgern an und fragt ab welcher gewipet werden soll
function ask_4_device(){
[ -e /tmp/devicelist ] || rm /tmp/devicelist
lsblk -o NAME,SIZE,TYPE,FSTYPE | tail -n+2 | tr -cd ',.\n [:alnum:]' | awk '{printf "%-5s%6s %s (%s) \n" , $1,$2,$3,$4}' | sed -e "s/()//g" >/tmp/devicelist
devlines=$(( $(cat /tmp/devicelist | wc -l) + 2 ))
dialog --backtitle "CERTBw - Zero-Wipe" --begin 2 $(mitte 30) --title "Available Devices" --progressbox $devlines 30 --and-widget --stdout --inputbox 'Welche Platte soll gewipet werden?' 7 60 '/dev/sda' < /tmp/devicelist
result=${?}
return $result
}

#prüft den rückgabewert des vorangegangenen 'dialog' fensters auf abbruch und startet das menu neu
function check_result(){
	result=${?}
	if ([ $result = 1 ] || [ $result = 255 ]); then
		info 'CANCELED' 1
		menu
		exit 0
	fi
}

#kopiert Nullen auf das Angegebene Gerät und zeitg den Fortschritt mit 'dialog' an
function wipe(){
	#anlegen von named pipes für den Datenstrom und Statusmeldungen
	mkfifo data
	mkfifo status

	size_512=$(blockdev --getsz $1)
	size=$((512 * ${size_512}))

	echo "wiping Disk $1:"
	(while read -r line
	do
		#Zusammenfassen von Informationen für das Dialogfenster in ein 'dialog' kompatibles Format
		split=$(echo $line | tr -d "%[]=<>" | xargs)
		
		space=$(echo "$split" | cut -f1 -d" ")
		time=$(echo "$split" | cut -f2 -d" ")
		rate=$(echo "$split" | cut -f3 -d" ")
		prozent=$(echo "$split" | cut -f4 -d" ")
		eta=$(echo "$split" | cut -f6 -d" ")
		echo "XXX"
		echo $prozent
		echo "Wiped $space in $time so far. ($rate)"
		echo "ETA : $eta"
		echo "XXX"
	done < <(pv -f -s $size /dev/zero 1>data 2>status | dd bs=1M iflag=fullblock oflag=nocache if=data of=$1 2>/dev/null | stdbuf -oL tr  "\r" "\n" <status) ) | dialog --backtitle "CERTBw - Zero-Wipe" --title "Wiping  $1" --gauge "Please wait" 7 70 0
	rm data
	rm status
}

function menu(){
	menu=$(dialog --stdout --backtitle "CERTBw - Zero-Wipe" --title "Wiping Complete" --menu "Action:" 0 0 5 1 Reboot 2 Poweroff 3 Verify 4 Re-Wipe 5 Shell)
	case "$menu" in
	1)	info "REBOOTING" 1; reboot
		exit 0
		;;
	2)	info "SHUTTING DOWN" 1; poweroff
		exit 0
		;;
	3)	info "Verify - Not yet implemented" 3
		menu
		;;
	4)	/etc/wipe.sh
		exit 0
		;;
	5)	exit 0
		;;
	*)	info 'CANCELED' 1
		exit 0
		;;
	esac
}

##simpler ablauf 
drive=$(ask_4_device)
check_result
wipe $drive
menu
exit 0
