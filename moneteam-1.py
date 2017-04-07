import pymonetdb

conn = pymonetdb.connect(database="voc",username="monetdb", password="monetdb",hostname="moneteam-1.csse.rose-hulman.edu")
cursor = conn.cursor()
print(cursor.execute("SELECT * FROM goodluck"))

