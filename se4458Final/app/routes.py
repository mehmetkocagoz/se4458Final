from flask import render_template,request,session,redirect,url_for
from app import app
from app.validation import checkUser
from app.blooddb import addBloodToDatabase,createDonorInDatabase,requestBloodFromDatabase


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
    branch_name = session['username']
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            
            return render_template("addblood.html",branch_name = branch_name)
        else:
            return redirect(url_for('login'))
    # Else if method is POST, it means form submitted and we will handle form operations
    else:
        blood_type = request.form['bloodType']
        unit = int(request.form['unit'])
        donor_name = request.form['donorName']
        print(blood_type)
        messageFromDatabase = addBloodToDatabase(donor_name,blood_type,unit)
        return render_template("addblood.html",branch_name = branch_name,message = messageFromDatabase)

@app.route("/create",methods = ['GET','POST'])
def createDonor():
    branch_name = session['username']
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            
            return render_template("createdonor.html",branch_name = branch_name)
        else:
            return redirect(url_for('login'))
    else:
        donor_name = request.form['donorName']
        blood_type = request.form['bloodType']
        city = request.form['city']
        town = request.form['town']
        email = request.form['email']
        phone = request.form['phone']
        
        messageFromDB = createDonorInDatabase(donor_name,blood_type,city,town,email,phone)
        return render_template("createdonor.html",branch_name = branch_name,message = messageFromDB)


@app.route("/userLogged")
def userOpt():
    return render_template("loggedFrame.html")


@app.route("/request",methods = ['GET','POST'])
def requestBlood():
    if request.method == 'GET':
        return render_template("requestblood.html")
    else:
        requestor = request.form['requestor']
        blood_type = request.form['bloodType']
        city = request.form['city']
        town = request.form['town']
        email = request.form['email']
        units = int(request.form['units'])
        duration = request.form['duration']
        reason = request.form['reason']
        donor_list = requestBloodFromDatabase(requestor,blood_type,city,town,email,units,duration)
        return render_template("requestblood.html",donors= donor_list)