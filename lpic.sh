#!/bin/bash
index=0
cat $@ | hxselect .qtext -s "@TKE@" | tr -d "\n" | tr -s " " | sed -e 's/@TKE@/\n/g' | while read block; do
(( index++ ))
echo "Frage $index"
echo "=================="
frage=$(echo $block | hxnormalize -e |  sed -ne '/div class=qtext/,/div class=answer/p' | html2text)
echo $frage
echo "Antworten:"
answ=$(echo $block | hxnormalize -e | hxselect .answers )
echo $answ
echo "Erklärung:"
expl=$(echo $block | hxnormalize -e | hxselect .explanation )
echo $expl
echo "=================="
echo "=================="

done
