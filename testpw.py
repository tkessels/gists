import sys
import hashlib
import requests

if len(sys.argv) != 2:
    print("Usage: python testpw.py <password>")
    exit(1)

url="https://api.pwnedpasswords.com/range/"
hash_object = hashlib.sha1(sys.argv[1].encode("UTF-8"))
pw_hash=hash_object.hexdigest()
first_part=pw_hash[:5]
second_part=pw_hash[5:]
print(pw_hash)
furl="{}{}".format(url,first_part)
print("Das gehashte Passwort lautet: {}".format(pw_hash))
print("Es werden lediglich die ersten 5 Zeichen des Hashes übertragen ({})".format(first_part))
print("Dies lässt keinerlei Rückschlusse auf da Passwort zu.")
response=requests.get(furl)
for line in response.text.splitlines():
    if second_part.lower() in line.lower():
        print("Passwort wurde {} mal im Datenbestand gefunden".format(line.split(":")[1]))
        exit(0)

print("Passwort wurde nicht im Datenbestand gefunden")
