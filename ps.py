import socket as sk
import sys
print(sys.argv)
print(len(sys.argv))
print("Host:" , sys.argv[1])
default=(21,22,23,80,110,111,135,139,389,443,515,631,3306,3389)

def usage():
	print("Usage:",sys.argv[0],"<ip> ( [<start_port> - <end_port] | [<port>] ) ")

if (len(sys.argv)==5) and sys.argv[3]=='-':
	 try:
	  ports=range(int(sys.argv[2]),int(sys.argv[4]))
	 except:
	  usage()
	  ports=default
elif len(sys.argv)>2:
	ports=sys.arv[2:]
else:
	ports=default

print("Ports:", ports)
for port in ports:
	try:
		s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
		s.settimeout(1)
		s.connect((sys.argv[1],port))
		print('%d:OPEN' % port)
		s.close
	except: continue
