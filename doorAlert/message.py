import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request
from twilio import twiml
from twilio.rest import TwilioRestClient
import time


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)


sh = client.open("form responses").sheet1 # way to open the google sheets
sh2= client.open("Database of members").sheet1

# Extract and print all of the values
list_of_hashes = sh.get_all_records() # finds all value in the google sheets
list_of_records= sh2.get_all_records() # gets all values of the sh2 google sheet


lastValue= list_of_hashes[-1] # finds last value in google sheeting
phone= lastValue["phonenumber"] # grabs their phone number
firstName= lastValue["firstname"] # grabs their first name
lastname= lastValue['lastname']
email= lastValue["email"] # grabs their email


print(firstName, lastname, " made the last response")
time.sleep(1)

grabVal= sh2.find(email) #this line will try to find the email inputed by the user in the google form
print("Searching google sheets with the following email for their phone number;", email)
row= grabVal.row # grabs the row of the email
col= grabVal.col # grabs the column of the email
MeetphoneNumber= sh2.cell(row, col+1).value #moves the column value one to the right to find the phone number
MeetfirstName= sh2.cell(row, col-3).value

#deleting the periods in the phone number in order to not cause problems with twilio
phones=[]
for x in MeetphoneNumber:
    if x !=".":
        phones.append(x)
compNum= ''.join(phones)

time.sleep(1)
print(MeetfirstName,"'s phone number is", compNum)
time.sleep(1)
print("Sending", MeetfirstName, "a text message")

ACCOUNT_SID = "AC3bd3a69773f1ea33cb499e04597dcebe"
AUTH_TOKEN = "5fc24bcb11f279efe7e608296bc74093"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to="+1"+compNum,
    from_="+19088458499",
    body= firstName+" "+lastname+" is waiting for you at the front desk!"
    )
