from scapy.all import srp, Ether, ARP
from threading import Thread
from ipaddress import IPv4Network
from pprint import pprint
from time import sleep, time

threads = []

clients = list()
class Scanner(Thread):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        # The below code from https://www.thepythoncode.com/article/building-network-scanner-using-scapy
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ip)
        # this is a tuple, which index 0 is host that answers arp request.
        # while index 1 is unanswered when no host answers arp request.
        result = srp(packet, timeout=3, verbose=0)[0]
        # the result is a tuple with index 0 as sent, and 1 as received.
        for _, received in result:
            # psrc is the arp responder's ip address
            # hwsrc is the arp responder's mac address
            clients.append(
                {
                    "ip": received.psrc,
                    "mac": received.hwsrc
                }
            )
        # maintain consistency by forcing this method to sleep for 1 second
        # before beginning the next host.
        sleep(1)


if __name__ == "__main__":
    start = time()
    for ip in IPv4Network('192.168.178.0/24').hosts():
        t = Scanner(str(ip))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    pprint(clients)
    print(f"Executed in {time() - start} seconds.")