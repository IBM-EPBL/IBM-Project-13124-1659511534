# importing the required libraries
from __future__ import division, print_function

import os

import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, session, redirect, url_for

#REST API

from flask_restful import Resource,Api
from keras.applications.inception_v3 import preprocess_input
from keras.models import model_from_json
from werkzeug.utils import secure_filename

#connection to database mysql
import MySQLdb
from flask_mysqldb import MySQL
import MySQLdb.cursors

global graph
graph=tf.compat.v1.get_default_graph()

# For Prediction in Server Console
predictions = ["Corpse Flower",
               "Great Indian Bustard",
               "Lady's slipper orchid",
               "Pangolin",
               "Spoon Billed Sandpiper",
               "Seneca White Deer"
              ]
#LInk For THose Predictions
found = [
        "https://en.wikipedia.org/wiki/Amorphophallus_titanum",
        "https://en.wikipedia.org/wiki/Great_Indian_bustard",
        "https://en.wikipedia.org/wiki/Cypripedioideae",
        "https://en.wikipedia.org/wiki/Pangolin",
        "https://en.wikipedia.org/wiki/Spoon-billed_sandpiper",
        "https://en.wikipedia.org/wiki/Seneca_white_deer",
        ]




#Initializing The Flask App

app=Flask(__name__)

app.secret_key='efghijk'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='digitalnaturalist'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/loginpage')
def loginpage():
    return render_template('login.html')
@app.route('/registerpage')
def registerpage():
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    msg=''
    if request.method =='POST' and 'Email' in request.form and 'Subject'in request.form:
        email= request.form['Email']
        password= request.form['Subject']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM validation1 WHERE Email= % s AND Password = % s',(email,password,))
        user=cursor.fetchone()
        if user:
            session['loggedin']=True
            session['Name']=user['Name']
            session['Email']=user['Email']
            msg='LOGGED IN SUCCESSFULLY'
            return render_template('upload.html',msg=msg)
        else:
            msg="PLEASE ENTER CORRECT EMAIL OR PASSWORD"
    return render_template('login.html',msg=msg)
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('Email', None)
    session.pop('loggedin',None)
    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])

def register():
    msg=''
    if request.method=='POST' and 'Name' in request.form and 'Email' in request.form and 'Password' in request.form and 'RetypePassword' in request.form:

        username=request.form.get('Name')
        email=request.form.get('Email')
        password=request.form.get('Password')
        password1=request.form.get('RetypePassword')
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM validation1 WHERE Email= % s and Password=% s", (email,password))
        account=cursor.fetchone()

        if account:
         msg= "Already Registered"
        elif not username or not email or not password or not password1:
            msg="Please register"
        elif not username:
            msg="Please Enter The UserName"
        elif not email:
            msg="Please Enter The  Email"
        elif  not password or not password1:
            msg="PLease Enter The Password"
        else:
            if password==password1:
                cursor.execute('INSERT INTO validation1(Name,Email,Password,Password1) VALUES (%s,%s,%s,%s)',(username,email,password,password1))
                mysql.connection.commit()
                msg= "you have successfully registered"

            else:
                msg=" Password MisMatched"
    elif request.method == 'POST':
         msg='please fill ou the form !'
    return render_template('register.html',msg=msg)

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return ("<h6 style=\"font-face:\"Courier New\";\">No GET request herd.....</h6 >")
    if request.method == 'POST':
        # Fetching the uploaded image from the post request using the id 'uploadedimg'
        f = request.files['uploadedimg']
        basepath = os.path.dirname(__file__)
        print(basepath)
        #Securing the file by creating a path in local storage
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        print(file_path)
        #Saving the uploaded image locally
        f.save(file_path)
        #loading the locally saved image
        img = tf.keras.utils.load_img(file_path, target_size=(224, 224))
        #converting the loaded image to image array
        x = tf.keras.utils.img_to_array(img)
        x = preprocess_input(x)
        # Converting the preprecessed image to numpy array
        inp = np.array([x])
        with graph.as_default():
            #loading the saved model from training
            json_file = open("DigitalNaturalist.json", 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            #adding weights to the trained model
            loaded_model.load_weights("DigitalNaturalist.h5")
            #predecting the image
            preds =  np.argmax(loaded_model.predict(inp),axis=1)
            #logs are printed to the console
            print("Predicted the Species " + str(predictions[preds[0]]))
        text = found[preds[0]]
        return redirect(text)



if __name__ == '__main__':
    #Threads enabled so multiple users can request simultaneously
    #debug is turned off, turn on during development to debug the errors
    #application is binded to port 8000
    app.run(threaded = True,debug=True,port="4000")


