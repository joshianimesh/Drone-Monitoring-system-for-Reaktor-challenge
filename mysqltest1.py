import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = '1234',
    database = 'reaktorchallenge'

)

mycursor = db.cursor()
#mycursor.execute("CREATE TABLE offenders(Time TIME(1),SerialNo VARCHAR(16), name VARCHAR(60), email VARCHAR(320), distance VARCHAR(40), phoneNumber VARCHAR(16))")
#mycursor.execute("DROP TABLE offendingPilots")
mycursor.execute("SELECT * FROM offenders")
result = mycursor.fetchall()
for x in result:
    print(x)
    print("\n")
    