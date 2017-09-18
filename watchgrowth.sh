#!/bin/bash


old_size=$(du -b "${1}" | cut -f1)
while true; do
sleep 1
new_size=$(du -b "${1}" | cut -f1)
size_diff=$(( ${new_size} - ${old_size} ))
old_size=${new_size}
#speed=$(( ${size_diff} / (1024*1024) ))
progress=""

if [[ $# -eq 2 ]] ; then
total=${2}
progress_p=$(echo "2 k ${new_size} ${total} 100 / / p" | dc)
progress="${progress_p} %"
fi

speed=$(echo "2 k ${size_diff} 1024 1024 * / p" | dc)

echo "${progress} - ${speed} MB/s"
done
