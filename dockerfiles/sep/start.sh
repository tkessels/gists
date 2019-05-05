#!/bin/bash
case "${1}" in
  shell )
    echo "stage: ${1}"
    service rtvscand start
    echo "Usage:"
    echo "sav manualscan -c <file>"
    /bin/bash
    ;;
  version )
    echo "stage: ${1}"
    service rtvscand start
    sleep 5
    sep_dev=$(sav info -d | tr -d '\r\n')
    sep_vers=$(sav info -p | tr -d '\r\n' )
    docker_tag=$(echo -n "${sep_dev}" | sed -e 's/rev./_/' -e 's/ //g' -e 's|/|.|g' -e 's/\([0-9]\{2\}\).\([0-9]\{2\}\).\([0-9]\{2\}\)/\2.\1.\3/g' )
    kernel_vers=$(uname -r)
    os_vers=$(head /etc/issue)
    echo "OS version: ${os_vers}"
    echo "Kernelversion: ${kernel_vers}"
    echo "Virusdefinition: ${sep_dev}"
    echo "Productversion: ${sep_vers}"
    echo "Dockertag: ${docker_tag}"
    echo "Java Version:"
    java -version

    ;;
  scan )
    echo "stage: ${1}"
    service rtvscand start
    sleep 5
    sav manualscan -c /data
    ;;
  tag )
    cat /root/tag
    ;;
  debug )
    echo "stage: ${1}"
    /bin/bash
    ;;
esac
