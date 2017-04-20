import pymonetdb
#import redis
#import pymongo

#redisConn = redis.Redis()
#mongoConn = pymongo.MongoClient()
monetConn = pymonetdb.connect(database="moneteamdb3",username = "monetdb", password = "moneteamPhrase433", hostname = "moneteam-3.csse.rose-hulman.edu")


def main():
    print("Welcome the StoreScheduler, by Moneteam.")
    command = ""
    while(True):
        command = raw_input("Scheduler>> ")
        if (command == 'quit'):
            break
        elif (command == 'help'):
            printhelp()
        else:
            handle(command)


def printhelp():
    print("To add an employee, type: \'add-emp <Name> <ID> <Age> <Wage>\'.")
    print("To get a list of employees, type: \'get-emp\'.")

def handle(command):
    args = command.split(" ")
    if args[0] == "add-emp":
        addEmp(args[1],args[2],args[3],args[4])
    elif args[0] == "get-emp":
        getEmp()

    else:
        printhelp()


def addEmp(name,empid,age,wage):
    cursor = monetConn.cursor()
    res = cursor.execute("insert into employee values (name,empid,age,wage) (\'%s\',%s,%s,%s)" % (name,empid,age,wage))
    if res == 1:
        print("The employee has been added.")

def getEmp():
    cursor = monetConn.cursor()
    cursor.execute("select * from employee")
    for x in cursor.fetchall():
        print(x) 


if __name__ == '__main__':
    main()
