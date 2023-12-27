from flask import render_template,request
from app import app

@app.route("/",methods = ['GET'])
def home():
    return render_template("index.html")

@app.route("/add")
def addBlood():
    return render_template("addblood.html")

@app.route("/create")
def createDonor():
    return render_template("createdonor.html")