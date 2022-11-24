# importing the required libraries


import os

import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, session, redirect, url_for

# connection to database mysql
import MySQLdb
from flask_mysqldb import MySQL
import MySQLdb.cursors


# Initializing The Flask App

app = Flask(__name__)

app.secret_key = 'efghijk'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'digitalnaturalist'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/loginpage')
def loginpage():
    return render_template('login.html')


@app.route('/registerpage')
def registerpage():
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Email' in request.form and 'Subject' in request.form:
        email = request.form['Email']
        password = request.form['Subject']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM validation1 WHERE Email= % s AND Password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['Name'] = user['Name']
            session['Email'] = user['Email']
            msg = 'LOGGED IN SUCCESSFULLY'
            return render_template('upload.html', msg=msg)
        else:
            msg = "PLEASE ENTER CORRECT EMAIL OR PASSWORD"
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('Email', None)
    session.pop('loggedin', None)
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'Name' in request.form and 'Email' in request.form and 'Password' in request.form and 'RetypePassword' in request.form:

        username = request.form.get('Name')
        email = request.form.get('Email')
        password = request.form.get('Password')
        password1 = request.form.get('RetypePassword')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM validation1 WHERE Email= % s and Password=% s", (email, password))
        account = cursor.fetchone()

        if account:
            msg = "Already Registered"
        elif not username or not email or not password or not password1:
            msg = "Please register"
        elif not username:
            msg = "Please Enter The UserName"
        elif not email:
            msg = "Please Enter The  Email"
        elif not password or not password1:
            msg = "PLease Enter The Password"
        else:
            if password == password1:
                cursor.execute('INSERT INTO validation1(Name,Email,Password,Password1) VALUES (%s,%s,%s,%s)',
                               (username, email, password, password1))
                mysql.connection.commit()
                msg = "you have successfully registered"

            else:
                msg = " Password MisMatched"
    elif request.method == 'POST':
        msg = 'please fill ou the form !'
    return render_template('register.html', msg=msg)


@app.route('/predict', methods=['GET', 'POST'])
def upload():
	return render_template("upload.html")
   
if __name__ == '__main__':
    app.run(threaded=True, debug=True, port="5000")


