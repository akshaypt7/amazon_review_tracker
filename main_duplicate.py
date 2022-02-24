# import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from replit import db
import pandas as pd
from tabulate import tabulate
from collections import OrderedDict

import warnings
warnings.filterwarnings("ignore") # we might have to remove this later, since we do not know if there might be any issues

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


chrome_options.add_argument("--headless") # running selenium in background

print('working with replit db')
driver = webdriver.Chrome(options=chrome_options)

# 

def db_empty(db):
  try :
    list_of_asins = list(db['ASIN'])
    return db
    
  except:
    print('Database is empty, we are adding asin : B07ZVXZNVD ')
    db['ASIN'] = ['B07ZVXZNVD']
    return db

db = db_empty(db)

def user_input(db):
  while True:
    list_of_asins = list(db['ASIN'])
    print(f'ASINs currently being tracked : {list_of_asins}')
    user_ans= str(input('Do you want to enter new ASINs to track reviews- yes or no : '))
    user_ans = user_ans.lower()   
    if user_ans == 'yes' or user_ans == 'no':
      break
    else:  
     print('Type either yes or no to Continue')  
  
  if user_ans == 'yes':
    print('Pass the ASIN of products you need to track the reviews')

    # list_of_asins = list(db['ASIN'])
    while True:
      new_asin = str(input('Enter Asin : '))
      if new_asin in list_of_asins:
        print('ASIN already being tracked')
        continue
        # there is an issue here if customer do not have any asin to add this might be infinite loop
      list_of_asins.append(new_asin)
      


      user_continue = str(input('Do you need to enter more ASINs - yes or no : ' ))
      user_continue = user_continue.lower() 

      
      while user_continue != 'no' and user_continue !='yes' :
        print('Enter either (yes/no)')
        user_continue = str(input('Do you need to enter more ASINs (yes or no) : ' ))
        user_continue = user_continue.lower()

      if user_continue =='no':  
        return list_of_asins

  else:
    # list_of_asins = list(db['ASIN'])
    return list_of_asins

        
        
      
list_of_asins = user_input(db)      
  

# list_of_asins = ['B07ZVXZNVD']
# list_of_asins = ['B07ZVXZNVD', 'B09CMWSVTH' ,'B09L64FT8X' ]

db['ASIN'] = list_of_asins

print('processing')

today = date.today()


list_of_reviews_per_asin = []
list_positive_reviews_per_asin =[]


web_url = 'https://www.amazon.in/dp/'


def browser(list_of_asins,web_url):

  while True:
    
    for asin in list_of_asins :
        
    
      new_url = web_url+ asin
      print(f'Checking the ratings of {asin} ...')
      driver.get(new_url)
      time.sleep(1)
      try: 
        driver.find_element_by_id('acrCustomerReviewText').click()
      except:
        print(f'There is an issue with {asin} Asin ')
        list_of_reviews_per_asin.append('error with asin')
        list_positive_reviews_per_asin.append('error with asin')
        continue
    
      
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
      
    
      total_percentage_of_neg_ratings = percentage_1star + percentage_2star + percentage_3star
      # print('total_percentage_of_neg_ratings ' + str(total_percentage_of_neg_ratings))
      total_neg_ratings = int(total_percentage_of_neg_ratings *0.01* total_ratings)
    
      
      five_star_ratings = int(percentage_5star*0.01*total_ratings)
    
    
      list_of_reviews_per_asin.append(total_neg_ratings)
      list_positive_reviews_per_asin.append(five_star_ratings)
      
      time.sleep(1)
      
      
    
    
    today_neg = str(today) + '_neg'
    today_pos = str(today) + '_pos'
    db[today_neg] = list_of_reviews_per_asin
    db[today_pos] = list_positive_reviews_per_asin
    return db

def today_tracked(). # function to see if the tracker was already ran today

db = browser(list_of_asins,web_url)



def create_table(db):
  dict = OrderedDict()

  for key in db.keys():
    dict[key]= list(db[key])

  print(tabulate(dict,headers='keys',tablefmt='fancy_grid')) 

create_table(db)

def delete_asin(db): # not done
  user_input_delete = str(input('Do you want to delete any asin from the table (yes/no) : '))
  user_input_delete = user_input_delete.lower() 

  while user_input_delete != 'no' and user_input_delete !='yes' :
    print('Enter either (yes/no)')
    user_input_delete = str(input('Do you want to delete any asin from the table (yes/no) : '))
    user_input_delete = user_input_delete.lower()

  if user_input_delete =='no':
    return None

  else:
    asin_input = str(input('Enter the Asin you want to delete : '))
    idx = db['ASIN'].index(asin_input)
    
    for key in db.keys():

      try:
        db[key].pop(idx)
        
      except:
        pass

  create_table(db)   
  
delete_asin(db)    


driver.quit()