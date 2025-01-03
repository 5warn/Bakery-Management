import mysql.connector
from mysql.connector import (connection)
def signup(name,email,password):
    cnn = connection.MySQLConnection(user='root', password='root',host='127.0.0.1',database='bakery')
    cursor=cnn.cursor()
    try:
        cursor.execute("insert into login(name,email,password,role) values(%s,%s,%s,%s)",(name,email,password,"u"))
        return "Success"
    except:
        return "Email already exists"
    finally:
        cnn.commit()
        cursor.close()
        cnn.close()
def signin(email,password):
    cnn = connection.MySQLConnection(user='root', password='root',host='127.0.0.1',database='bakery')
    cursor=cnn.cursor()
    cursor.execute("select * from login where email=%s and password=%s",(email,password))
    data=cursor.fetchone()
    if data is None:
        return "invalid" 
    else:
        return data[3]
    cursor.close()
    cnn.close()
#print(signin("swarn@12.com","me"))
#print(signin("admin123@gmail.com","admin123"))
#signup("sai","sai@gmail.com","sai")
print("hi")
