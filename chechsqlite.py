import sqlite3
import sys
import re
dbfile=sys.argv[1]
# dbfile="/home/skyhawk/Documents/test.db"

try:
    db=sqlite3.connect(dbfile)
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables=cur.fetchall()
    # for row in db.execute("pragma table_info('sqlite_master')").fetchall():
    #     print(row)
    nice_tables={}
    for table in tables:
        # print(table)
        nice_rows=[]
        for row in db.execute("pragma table_info(" + str(table[0]) +")").fetchall():
            # print(row[1])
            if re.match('hash|pass',row[1], re.IGNORECASE):
                nice_rows.append(row[1])
            if len(nice_rows) > 0:
                nice_tables[table[0]]=nice_rows



except Exception as e:
    # print("Error opening DB %s" % dbfile)
    # sys.std.write(e)
    exit(1)

print("[+] %s is Valid DB " % dbfile)
if len(nice_tables)>0:
    for tab in nice_tables:
        print(nice_tables[tab])

db.close()
