import os

from models import *
from flask import render_template,request
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import datetime

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
    return render_template("index.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.form['action'] == 'register' :
        
        user_name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("psw")
        #password = password.encode("UTF-8")
        #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        time_stamp = datetime.datetime.now()
        user = Users(username = user_name,email= email,password= password, timestamp=time_stamp)
        try:
            db.session.add(user)
            db.session.commit() 
            return render_template("success.html", name=user_name)
        except exc.IntegrityError:
            flag = 1
            return render_template("register.html", flag = flag, message = "Username already exists. Please give another name")
        # except:
        #     flag = 2
        #     return render_template("register.html", flag = flag, message = "something went wrong.Please register again")

