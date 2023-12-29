from flask import render_template,request,session,redirect,url_for
from app import app
from app.validation import checkUser


app.secret_key = 'random_string'

@app.route("/",methods = ['GET'])
def home():
    return render_template("index.html")

@app.route("/login", methods = ['GET','POST'])
def login():
    # If request method is POST, it comes froms the form, check database and validate user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if checkUser(username,password):
            session['logged_in'] = True
            session['username'] = username
            
            return redirect(url_for('userOpt'))
        else:
            error = 'Wrong username or password'
            return render_template("login.html",error=error)
    # else it is a GET request and we will render login page
    else:
        return render_template("login.html")

@app.route("/add",methods = ['GET','POST'])
def addBlood():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            branch_name = session['username']
            return render_template("addblood.html",branch_name = branch_name)
        else:
            return redirect(url_for('login'))
    # Else if method is POST, it means form submitted and we will handle form operations
    else:
        return "a"

@app.route("/create")
def createDonor():
    if 'logged_in' in session and session['logged_in']:
        branch_name = session['username']
        return render_template("createdonor.html",branch_name = branch_name)
    else:
        return redirect(url_for('login'))

@app.route("/userLogged")
def userOpt():
    return render_template("loggedFrame.html")


@app.route("/request")
def requestBlood():
    return render_template("requestblood.html")