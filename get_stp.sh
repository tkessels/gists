#!/bin/bash
interface=${1}
one_stp=$(timeout -k 10 10 tcpdump -vvv -c1 stp -i ${interface} 2>/dev/null)
root_id=$(echo "$one_stp" | grep -Po "(?<=root-id )[^,]*")
bridge_id=$(echo "$one_stp" | grep -Po "(?<=bridge-id )[^,]*" | cut -f1 -d. )
port_id=$(echo "$one_stp" | grep -Po "(?<=bridge-id )[^,]*" | cut -f2 -d. )

echo "connected over $bridge_id at $port_id to $root_id"
echo $one_stp

if [[ $root_id == "80a3.00:1d:71:b9:f0:80" ]]; then
  echo "iassc detected"
fi
#bridge-id c0a3.d0:c7:89:94:b4:00.8009
#bridge-id c0a3.d0:c7:89:94:b4:00.8009
