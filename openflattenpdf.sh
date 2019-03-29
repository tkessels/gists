#!/usr/bin/env bash

tmpfile=$(mktemp)
pdf2ps "${1}" - | ps2pdf - "${tmpfile}"
evince ${tmpfile}
