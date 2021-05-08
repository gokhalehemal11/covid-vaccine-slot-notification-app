# importing the required libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime
import random


def switchHeader():
	headersList= [
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			]

	return random.choice(headersList)

def switchLanguage():
	langList= ['en-US', 'hi-IN']
	return random.choice(langList)

def setuAPIReq(URL, PARAMS, HEADERS= {}):

	r = requests.get(URL, headers= HEADERS, params= PARAMS, timeout=5)
	if r.status_code == 200:
		print(r)
	else:
		HEADERS = {
    	'User-Agent': switchHeader(),
		'accept-Language': switchLanguage(),
		'content': 'application/json'
		}
		ret= setuAPIReq(URL, PARAMS, HEADERS)

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

		print("Pincode "+str(pincode)+" API Call: ")
		setuAPIReq(URL, PARAMS)
		print()

	for district_id in sort_by_district.keys():

		PARAMS= {'district_id': district_id, 'date': today_date}
		URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

		print("District "+str(district_id)+" API Call: ")
		setuAPIReq(URL, PARAMS)
		print()

if __name__ == '__main__':
	GetDataFromSetuAPI()
