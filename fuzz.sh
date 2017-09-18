#!/bin/bash
pattern='\b(([01]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}([01]?\d{1,2}|2[0-4]\d|25[0-5])\b'
#count ips in log
count=$(cat $1 | grep -Po $pattern | sort -u  | wc -l)
#create ip_map for translation of IPs
paste <(cat $1 | grep -Po $pattern | sort -u) <(paste <(shuf <(for i in {0..255};do echo $i; done))  <(shuf <(for i in {0..255};do echo $i; done))  <(shuf <(for i in {0..255};do echo $i; done))  <(shuf <(for i in {0..255};do echo $i; done)) | tr "\t" "." | head -n $count) > ${1}.ip_map

#awk script to replace IPs
awk_script='
NR == FNR {
  rep[$1] = $2
  next
} 

{
  for (key in rep)
    gsub(key, rep[key])
  print
}
'
#OUTPUT
cat $1 | awk "$awk_script" ${1}.ip_map - 

echo "Lookup-Table is stored in ${1}.ip_map" >&2
