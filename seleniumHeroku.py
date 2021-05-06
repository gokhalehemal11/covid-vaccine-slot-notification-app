from selenium import webdriver
import os

options = webdriver.ChromeOptions()
options.binary_location= os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")

driver= webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), options= options)
driver.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=146&date=06-05-2021")
print(driver.page_source)
