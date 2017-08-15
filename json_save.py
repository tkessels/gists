import simplejson
import json

def put(data, filename):
    try:
        jsondata = simplejson.dumps(data, indent=4, skipkeys=True, sort_keys=True)
        fd = open(filename, 'w')
        fd.write(jsondata)
        fd.close()
    except Exception as e:
        print('ERROR writing', filename)
        print( e)
        pass

def get(filename):
    returndata = {}
    try:
        fd = open(filename, 'r')
        text = fd.read()
        fd.close()
        returndata = json.read(text)
        # Hm.  this returns unicode keys...
        #returndata = simplejson.loads(text)
    except:
        print('COULD NOT LOAD:', filename)
    return returndata


        # print(mail.filename)
        # print(mail.status)

# import gzip
# import json
#
# # writing
# with gzip.GzipFile(jsonfilename, 'w') as outfile:
#     for obj in objects:
#         outfile.write(json.dumps(obj) + '\n')
#
# # reading
# with gzip.GzipFile(jsonfilename, 'r') as isfile:
#     for line in infile:
#         obj = json.loads(line)
#         # process obj
# picklefile=open("mails.dump",'wb')
# for mail in list_of_mail:
#     pickle.dump(mail, picklefile )
#
# picklefile.close()

