import os
import bcrypt
from models import *
from flask import render_template,request,redirect
from flask import Flask,url_for,session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import datetime
import logging

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'name' not in session:
        return redirect(url_for('register'))
    elif session['name']:
        return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.form['action'] == 'register' : 
        user_name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("psw")
        password = password.encode("UTF-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        time_stamp = datetime.datetime.now()
        user = Users(username = user_name,email= email,password= hashed,timestamp=time_stamp)
        try:
            db.session.add(user)
            db.session.commit() 
            return render_template("success.html", name=user_name)
        except exc.IntegrityError:
            flag = 1
            return render_template("register.html", flag = flag, message = "Username already exists. Please give another name")
        except:
             flag = 2
             return render_template("register.html", flag = flag, message = "something went wrong.Please register again")
    elif request.form['action'] == 'login':
        authentication()


@app.route("/admin")
def admin():
    all_users = Users.query.order_by(Users.timestamp).all()
    return render_template("users.html", users = all_users)


@app.route("/authentication",methods=["GET","POST"])
def authentication():
    if request.method == "POST":
        name = request.form.get("name")
        #email = request.form.get("email")
        pwrd = request.form.get("psw")
        user_obj_name = Users.query.get(name)
        #print("Hello")
        #print(user_obj_name)
        if user_obj_name:
            #print("Hi")
            if pwrd == user_obj_name.password :
                session["name"] = name
                return redirect(url_for('index'))
            else :
                flag = 3
                return render_template("register.html", flag=flag,message = "Password doesn't match please give correct password")
        else :
            flag = 4
            return render_template("register.html", flag=flag, message="Username not found. Please register")

