#!/bin/bash
picture="${1}"
url="https://www.google.com/maps/place/$(exiftool -ee -p '$gpslatitude, $gpslongitude' -c "%d?%d'%.2f"\" ${picture} 2> /dev/null | sed -e "s/ //g" -e "s/?/%C2%B0/g")"
firefox -p work "$url"
