import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)


sheet1 = client.open("test").sheet1 # way to open the google sheets
foundValue= sheet1.find("jhonatan") #this will find the cell given the value provided
numberCell= foundValue.row # this will find the row value of foundValue

sheet2= client.open("test").sheet1 # sample sheet of responses

# Extract and print all of the values
list_of_hashes = sheet1.get_all_records() # finds all value in the google sheets
values_list = sheet1.row_values(1)
list_value =values_list.value 
sheet2= sheet2.get_all_records() #retriveing records from the second google sheet

# print(list_value)
# print(values_list)
print(list_of_hashes)
print(foundValue)
print(numberCell)
# print()
# print(sheet2)
