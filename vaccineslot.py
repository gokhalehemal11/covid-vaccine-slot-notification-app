# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime

def setuAPIReq(URL, PARAMS, HEADERS= {}):

	session = requests.Session()
	r = session.get(URL, headers= HEADERS, params= PARAMS, timeout=5)
	print(r.status_code)
	if r.status_code == 200:
		return r.json()
	else:
		HEADERS = {
    	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
		'accept-Language': 'en-US',
		'content': 'application/json'
		}
		setuAPIReq(URL, PARAMS, HEADERS)

def GetDataFromGoogleSheets():
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
	print("All records", records_data)
	print()

	sort_by_pincode= dict()
	sort_by_district= dict()
	for record in records_data:
		if record['District'] != '':
			if record['District'] not in sort_by_district:
				sort_by_district[record['District']]= [record]
			else:
				sort_by_district[record['District']].append(record)

		if record['Pincode'] != '':
			if record['Pincode'] not in sort_by_pincode:
				sort_by_pincode[record['Pincode']]= [record]
			else:
				sort_by_pincode[record['Pincode']].append(record)

	return [sort_by_district, sort_by_pincode]

def GetDataFromSetuAPI():
	# Get today's date
	today_date= datetime.today().strftime('%d-%m-%Y')

	sort_by_district, sort_by_pincode= GetDataFromGoogleSheets()

	print(sort_by_district)
	print()
	print(sort_by_pincode)

	for pincode in sort_by_pincode.keys():

		PARAMS= {'pincode': pincode, 'date': today_date}
		URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

		print("Pincode ", setuAPIReq(URL, PARAMS))
		print()

	for district_id in sort_by_district.keys():

		PARAMS= {'district_id': district_id, 'date': today_date}
		URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

		print("District ", setuAPIReq(URL, PARAMS))
		print()

if __name__ == '__main__':
	GetDataFromSetuAPI()
