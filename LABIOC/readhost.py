import sqlite3
hostlist=[]
iterator = open("allhost.txt")
for host in iterator:
    ithost = host.split()
    hostlist.append(ithost)


db=sqlite3.connect("db.sqlite3")
cursor=db.cursor()
query = "insert into LA_SHHost (owner, host_name) values (? , ?)"


for ithost in hostlist:
    owner = ithost[0]
    name = ithost[1]
    values = (str(owner), str(name))
    cursor.execute(query, values)

cursor.close()
db.commit()
db.close()

db=sqlite3.connect("db.sqlite3")
cursor=db.cursor()

cursor.execute("select * from LA_SHHost")
results=cursor.fetchall()
for row in results:
    print(row)

cursor.close()
db.commit()
db.close()
