#!/bin/bash
url=$(echo -ne "${*}" | grep -Pio -m1 'https://www.youtube.com/(watch\?[^&,|]+|embed/[^?/,|]+)')
if [[ -n "${url}" ]] ; then
title=$(wget -q -O- "${url}" | grep -Po "(?<=title>).*(?=</title)")
title_parsed=$(cat <<eof | python3
from urllib.parse import unquote
from html import unescape
url="${title}"
print(unescape(unquote(url)))
eof
)
echo "${url};\"${title_parsed}\""

fi
