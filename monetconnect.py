
import pymonetdb
conn = pymonetdb.connect(database = "voc", username = "monetdb", password = "monetdb", hostname = "moneteam-2.csse.rose-hulman.edu")

cursor = conn.cursor()
print(cursor)
#print(cursor.execute("select * from voctable"))
#cursor.execute('drop table victortable;')

cursor.execute('create table victortable (id int, val varchar(20));')
cursor.execute('insert into table victortable (id, val) values (11, \'hey\'), (12, \'jameswashere\');')
