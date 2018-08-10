#!/bin/bash
url=$(echo -ne "${*}" | grep -Pio -m1 'https://www.youtube.com/watch\?[^&|]+')
title=$(wget -q -O- "${url}" | grep -Po "(?<=title>).*(?=</title)")
title_parsed=$(cat <<eof | python3
from urllib.parse import unquote
import html
import sys
url="${title}"
print(html.unescape(unquote(url)))
eof
)

echo "${*};\"${title_parsed}\""
