# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('VaccineSlotApp')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get all the records of the data
records_data = sheet_instance.get_all_records()

# view the data
print(records_data)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
		'Connection': 'keep-alive',
    'Referer': 'www.cowin.gov.in',
    'accept': 'application/json',
		'accept-Language': 'en-US'
		}

PARAMS= {'pincode':'413608', 'date': '06-05-2021'}
URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=413608&date=06-05-2021"


session = requests.Session()
r = session.get(URL, headers=HEADERS, timeout=5)
print(r.status_code)
print(r.json())
