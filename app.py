from flask import Flask,render_template
import mysql.connector
app = Flask(_name_)
@app.route('/sign_in')
def sign_in():
    return render_template('fsign_in.html')
@app.route('/index')
def index():
    return render_template('findex.html')
@app.route('/sign_up')
def sign_up():
    return render_template('fsignup.html')
@app.route('/contact')
def contact():
    return render_template('fcontact.html')
@app.route('/menu')
def menu():
    return render_template('fmenu.html')
def sign_up(name,email,password):
    cnn = mysql.connector.connect(
        host = "localhost",user="root",password="rootuser",database="bakery")
    cursor = cnn.cursor()
    cursor.execute("insert into login(name,email,password,role) values(%s,%s,%s,%s)",(name,email,password,"u"))
    cnn.commit()
    cursor.close()
    cnn.close()
def sign_in(email,password):
    cnn = mysql.connector.connect(
        host = "localhost",user="root",password="root",database="bakery")
    cursor = cnn.cursor()
    cursor.execute("select * from login where email=%s and password=%s",(email,password))
    data = cursor.fetchone()
    if data is None:
        return "Invalid"
    else:
        return data[4]
    cursor.close()
    cnn.close()
print("hi")
#sign_up("Rahul","Ra@gmail.com","123")
