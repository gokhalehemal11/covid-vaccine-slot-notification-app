from selenium import webdriver
import os

options = webdriver.ChromeOptions()
options.binary_location= os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")
options.add_argument("Accept-Encoding=gzip, deflate, br")
options.add_argument("Accept-Language= en-US,en;q=0.9,mr;q=0.8")
options.add_argument("Host= cdn-api.co-vin.in")
options.add_argument("sec-ch-ua= ' Not A;Brand';v='99', 'Chromium';v='90', 'Google Chrome';v='90'")
options.add_argument("Connection= keep-alive")
options.add_argument("Accept= text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver= webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), options= options)
driver.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=146&date=06-05-2021")
print(driver.page_source)
