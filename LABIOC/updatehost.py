import sqlite3

db=sqlite3.connect("db.sqlite3")
cursor=db.cursor()



query = "update LA_SHHost set host_name='MSD-2880384' where id=4"

cursor.execute(query)
cursor.execute("select * from LA_SHHost")
results=cursor.fetchall()
for row in results:
    print(row)

cursor.close()
db.commit()
db.close()
