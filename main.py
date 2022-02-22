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
from replit import db
import pandas as pd

import warnings
warnings.filterwarnings("ignore") # we might have to remove this later, since we do not know if there might be any issues

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print('working with replit db')
driver = webdriver.Chrome(options=chrome_options)


# list_of_asins = ['B07ZVXZNVD']
list_of_asins = ['B07ZVXZNVD', 'B09CMWSVTH' ,'B09L64FT8X' ,'B0957WJB9N']

db['ASIN'] = list_of_asins


today = date.today()


list_of_reviews_per_asin = []
list_positive_reviews_per_asin =[]


web_url = 'https://www.amazon.in/dp/'


for asin in list_of_asins :
    

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

  #postive reviews
  percentage_5star = driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[1]/td[3]/span[2]/a').text
  percentage_5star = int(percentage_5star.split('%')[0])
  print(percentage_5star)

  total_percentage_of_neg_ratings = percentage_1star + percentage_2star + percentage_3star
  # print('total_percentage_of_neg_ratings ' + str(total_percentage_of_neg_ratings))
  total_neg_ratings = int(total_percentage_of_neg_ratings *0.01* total_ratings)

  
  five_star_ratings = int(percentage_5star*0.01*total_ratings)


  list_of_reviews_per_asin.append(total_neg_ratings)
  list_positive_reviews_per_asin.append(five_star_ratings)
  
  time.sleep(2)
  
  


today_neg = str(today) + '_neg'
today_pos = str(today) + '_pos'
db[today_neg] = list_of_reviews_per_asin
db[today_pos] = list_positive_reviews_per_asin

# print(db[today])

df = pd.DataFrame(columns = db.keys())

# there might be some issues in future here when more columns comes in

for col in df.columns:

  df[col]= db[col]

print(df)  

driver.quit()