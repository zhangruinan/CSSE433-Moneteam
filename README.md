# CSSE433-Moneteam
RHIT-Advanced Databases final project. Using multiple databases to create a scheduling assistant. 


moneteam-1 has access to repo. Added more text

# Examples of connecting to remote monetdb server through pymonetdb
>>> import pymonetdb
>>> conn = pymonetdb.connect(database="voc",username = "monetdb", password = "monetdb", hostname = "moneteam-3.csse.rose-hulman.edu")
>>> cursor = conn.cursor()
>>> cursor.execute("select * from voctable")
2

