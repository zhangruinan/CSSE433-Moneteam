#import pymonetdb
#conn = pymonetdb.connect(database = "moneteamdb1", username = "monetdb", password = "moneteamPhrase433", hostname = "moneteam-1.csse.rose-hulman.edu")

#cursor = conn.cursor()
print(cursor)
#print(cursor.execute("select * from voctable"))
#cursor.execute('drop table victortable;')
#
#cursor.execute('create table victortable (id int, val varchar(20));')
#cursor.execute('insert into table victortable (id, val) values (11, \'hey\'), (12, \'jameswashere\');')


import pymonetdb
conn = pymonetdb.connect(database="moneteamdb1", hostname="moneteam-1.csse.rose-hulman.edu")
curs = conn.cursor()
curs.execute("select * from testtable")
# -> 1 (num elements in query)
curs.fetchone()
# -> (11, u'hey')
