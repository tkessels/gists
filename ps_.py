import psutil
import os
import pwd
import sys
from collections import defaultdict

mypid=os.getpid()

#Check if run as root
white_list_pname = [ "systemd", "kthreadd", "apport-gtk"]
white_list_pid =[]

if (os.geteuid()) != 0:
    print("[-] Not Root")
else:
    #whitelist this python script and all parents
    cursor=psutil.Process()
    ende=0
    while cursor != None:
        white_list_pid.append(cursor.pid)
        cursor=cursor.parent()
    print(white_list_pid)

mydict = defaultdict(list)
ps_dict = defaultdict(list)

def on_terminate(proc):
    print("[+] Terminating Child: %s" % (str(proc)))

def killpid(pid):
    parent = psutil.Process(pid)

    print(len(parent.children()))
    children=parent.children(recursive=True)
    for child in children:
        try:
            child.terminate()
        except Exception as e :
            print("[-] FAILED - Terminating Child: %s" % (str(child)))
            print("[-] ERROR: %s" % str(e))


    gone, still_alive = psutil.wait_procs(children, timeout=3, callback=on_terminate)

    for child in still_alive:
        try:
            child.kill()
        except Exception as e :
            print("[-] FAILED - Terminating Child: %s" % (str(child)))
            print("[-] ERROR: %s" % str(e))
        else:
            print("[+] Terminating Child: %s" % (str(child)))
    try:
        parent.terminate()
        parent.wait(timeout=3)
        parent.kill()
    except Exception as e:
        print("[-] FAILED - Killing Process: %s" % (str(parent)))
        print("[-] ERROR: %s" % str(e))
    else:
        print("[+] Process Killes: %s" % (str(parent)))



def printproc(p: psutil.Process):
    return "{0}({1})".format(p.name(),p.pid())


def printchild(p: psutil.Process):
    output=printproc(p) + "-"
    for c in p.children():
        output+=printproc(c)


#Fill ps_dict with processes
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid','uids','ppid','name','create_time','terminal','username'])
    except psutil.NoSuchProcess:
        pass
    else:
        pid=str(pinfo['pid'])
        ps_dict[pid]=pinfo


#Walk ps_dict and fill in missing information
for key in ps_dict:
    p=ps_dict[key]
    ppid=str(p['ppid'])
    if ppid in ps_dict:
        pp=ps_dict[ppid]
        p['ppname'] = pp['name']
        p['ppusername'] = pp['username']
        p['ppuids'] = pp['uids']
        p['ppcreate_time'] = pp['create_time']


#Kill all escalators
to_kill=[]

for key in ps_dict:
    p=ps_dict[key]
    if 'ppusername' in p and 'real=0' in str(p['uids']) and p['username'] not in p['ppusername']:
        if p['name'] not in white_list_pname:
            print("[+] Escalted Process found: %s (%s)" % (str(p['name']),str(p['pid'])))
            printchild(psutil.Process(p['pid']))



for pid in to_kill:
    if pid not in white_list_pid:
        killpid(pid)
