# import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import openpyxl
from datetime import date

import warnings
warnings.filterwarnings("ignore") # we might have to remove this later, since we do not know if there might be any issues

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print('start')
driver = webdriver.Chrome(options=chrome_options)
# driver.get("https:/amazon.in")


path = 'reviews_tracker_sheet.xlsx'
workbook = openpyxl.load_workbook(path)
sheet = workbook.active
rows = sheet.max_row
cols = sheet.max_column
# print('columns = '+ str(cols))

today = date.today()
sheet.cell(row=2,column=2).value=today
# print(today)
workbook.save(path) 

web_url = 'https://www.amazon.in/dp/'

asin = sheet.cell(row=3,column=1).value
new_url = web_url+ asin

driver.get(new_url)

print('exit_1')

for row in range(3,rows+1):
    for col in range(1,2): 
        print(col)
        asin = sheet.cell(row=row,column=1).value
        asin = str(asin)
        new_url = web_url+ asin
        driver.get(new_url)
        driver.find_element_by_id('acrCustomerReviewText').click()
        string_review = driver.find_element_by_id('acrCustomerReviewText').text
        total_ratings = string_review.split()[0]
        total_ratings = int(total_ratings)

        percentage_1star = driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[5]/td[3]/span[2]').text
        percentage_1star = int(percentage_1star.split('%')[0]) # converting string into integer (ex: '20%' into 20)

        percentage_2star = driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[4]/td[3]/span[2]').text
        percentage_2star = int(percentage_2star.split('%')[0])

        percentage_3star = driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[3]/td[3]/span[2]').text
        percentage_3star = int(percentage_3star.split('%')[0])

        total_percentage_of_neg_ratings = percentage_1star + percentage_2star + percentage_3star
        # print('total_percentage_of_neg_ratings ' + str(total_percentage_of_neg_ratings))
        total_neg_ratings = int(total_percentage_of_neg_ratings *0.01* total_ratings)

        sheet.cell(row=row,column=2).value = total_neg_ratings
        time.sleep(2)
        print(total_neg_ratings)
        workbook.save(path)

print('exit-2')

workbook.save(path)
driver.quit()