# CSSE433-Moneteam
RHIT-Advanced Databases final project. Using multiple databases to create a scheduling assistant. 


moneteam-1 has access to repo. Added more text

#### Set monetdb to certain ip address
`monetdbd set port=0.0.0.0 yourDataFarm/ `

#### create a database in monetdb
`monetdb create db`

#### release a database in monetdb 
`monetdb release db`
### Examples of connecting to remote monetdb server through pymonetdb
```
import pymonetdb
conn = pymonetdb.connect(database="voc",username = "monetdb", password = "monetdb", hostname = "moneteam-3.csse.rose-hulman.edu")
cursor = conn.cursor()
cursor.execute("select * from voctable")
```

### Set mongoDB Replica Sets
```
rs.initiate()
rs.add("moneteam-X.csse.rose-hulman.edu:00000")

# set arbiter
rs.add("...",{arbiter:true})

# check heart beat
rs.status()

# allow read on secondary
rs.slaveOK()
```

