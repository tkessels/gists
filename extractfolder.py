import subprocess
import sys

image=sys.argv[1]
inode=sys.argv[2]


output = subprocess.check_output(f"fls -F {image} {inode}", shell=True)

output=output.decode()
result = {}
for row in output.split('\n'):
    if ':' in row:
        key, value = row.split(':')
        idx = key.split(" ")[-1]
        fsid = idx.split("-")[0]
        result[fsid] = value.strip()

for fsid in result:
    print(f"Writing Inode {fsid} -> {result[fsid]} ")
    outfile=open(result[fsid],'w')
    subprocess.run(["icat", image, fsid],stdout=outfile)

