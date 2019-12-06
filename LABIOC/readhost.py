import sqlite3
hostlist=[]
iterator = open("machinelist.txt")
for host in iterator:
    ithost = host.split()
    hostlist.append(ithost)


db=sqlite3.connect("db.sqlite3")
cursor=db.cursor()
query = "insert or ignore into LA_SHHost (owner, machine_name) values (? , ?)"


for ithost in hostlist:
    owner = r'Lab'
    name = ithost[0]
    values = (str(owner), str(name))
    cursor.execute(query, values)
    print(name)

cursor.close()
db.commit()
db.close()

db=sqlite3.connect("db.sqlite3")
cursor=db.cursor()

cursor.execute("select machine_name from LA_SHHost")
results=cursor.fetchall()
for row in results:
    print(row)

cursor.close()
db.commit()
db.close()
