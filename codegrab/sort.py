import os
import sys
import subprocess
import re

pattern=re.compile("(: )([^;]+)")
for file in os.listdir(sys.argv[1]):
    output=subprocess.check_output(["file","-Ni",file])
    match=pattern.search(output)
    mimetype=re.sub(r"\W","_",match.group(2))
    if not os.path.exists(mimetype):
        os.makedirs(mimetype)
    os.rename(file,mimetype+os.sep+file)
