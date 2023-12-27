from flask import render_template,request,session,redirect,url_for
from app import app
from app.validation import checkUser


app.secret_key = 'random_string'

@app.route("/",methods = ['GET'])
def home():
    return render_template("index.html")

@app.route("/login", methods = ['GET','POST'])
def login():
    # If request method is POST, it comes froms the form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if checkUser(username,password):
            session['logged_in'] = True
            session['username'] = username
            
            return redirect(url_for('userOpt'))
    else:
        return render_template("login.html")

@app.route("/add")
def addBlood():
    if 'logged_in' in session and session['logged_in']:
        return render_template("addblood.html")
    else:
        return redirect(url_for('login'))

@app.route("/create")
def createDonor():
    if 'logged_in' in session and session['logged_in']:
        return render_template("createdonor.html")
    else:
        return redirect(url_for('login'))

@app.route("/userLogged")
def userOpt():
    return render_template("loggedFrame.html")


@app.route("/request")
def requestBlood():
    return render_template("requestblood.html")