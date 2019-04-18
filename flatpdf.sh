#!/bin/bash
if ! which zathura 1>/dev/null  2>&1 ; then
  echo "zathura pdf viewer not found"
  echo "sudo apt install zathura"
  exit 1
fi

if ! which docker 1>/dev/null  2>&1 ; then
  echo "docker not found"
  echo "sudo apt install docker.io"
  exit 1
fi

if [[ -f "${1}" ]] ; then
  cat "${1}" | docker run -i --rm tabledevil/flatpdf | zathura -
fi
