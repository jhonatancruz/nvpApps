from flask import Flask, request, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pyvirtualdisplay import Display
import bs4 as bs
import urllib.request
import requests
from twilio import twiml
from twilio.rest import TwilioRestClient

app= Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def index(): #self,phones
    if request.method=="POST":
        name= request.form['name']
        proName= request.form['proName']
        verifyCompany()
        return render_template("success.html")
    return render_template("/index.html")


@app.route("/verifyCompany", methods=["GET", "POST"])
def verifyCompany():
        number="9082677299"
        name= request.form['name']
        proName= request.form['proName']

        ACCOUNT_SID = "AC3bd3a69773f1ea33cb499e04597dcebe"
        AUTH_TOKEN = "5fc24bcb11f279efe7e608296bc74093"


        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
            to="+1"+number,
            from_="+19088458499",
            body= "hi jhon waiting for you at the front desk"
            )


if __name__ =="__main__":
    app.run(debug=True)
