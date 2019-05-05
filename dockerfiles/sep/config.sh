service rtvscand start
echo "Starting Liveupdate"
sav liveupdate -u
echo "Done with Liveupdate"
echo "Changing Config for Manualscan"
key='\Symantec Endpoint Protection\AV\LocalScans\ManualScan'
cmd='/opt/Symantec/symantec_antivirus/symcfg'
#Setting AntivirusAction to just
${cmd} add -k "${key}" -v FirstAction -d 0 -t 'REG_DWORD'
${cmd} add -k "${key}" -v FirstMacroAction -d 0 -t 'REG_DWORD'
${cmd} add -k "${key}" -v Checksum -d 1 -t 'REG_DWORD'

while ! (sav info -d | grep -Pq '^\d') ; do
  sleep 1
done

#writing DefinitionVersion to file in TAGFORMAT
sav info -d | tr -d '\r\n' | sed -e 's/rev./_/' -e 's/ //g' -e 's|/|.|g' -e 's/\([0-9]\{2\}\).\([0-9]\{2\}\).\([0-9]\{2\}\)/\2.\1.\3/g' | tee /root/tag
service rtvscand stop
sleep 5
