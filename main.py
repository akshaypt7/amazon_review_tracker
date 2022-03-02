# import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
from replit import db
import pandas as pd
from tabulate import tabulate
from collections import OrderedDict
from email_csv import sent_email
import warnings
warnings.filterwarnings("ignore") # we might have to remove this later, since we do not know if there might be any issues

# To run selenium in Replit
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# running selenium in background
chrome_options.add_argument("--headless") 

# Initiating the driver object from selenium
driver = webdriver.Chrome(options=chrome_options)


def db_empty(db):
  '''We are checking if the database is empty, if it is we add one product to the database .'''
  
  try :
    list_of_asins = list(db['ASIN'])
    return db
    
  except:
  
    print('Database is empty, we are adding asin : B07ZVXZNVD \n')
    db['ASIN'] = ['B07ZVXZNVD']
    return db


db = db_empty(db)


def user_input(db=db):

  '''Here we ask for the input from the user to add new asins to track. We also display the ASINS we are tracking.'''
  
  while True:
    list_of_asins = list(db['ASIN']) # list of asins we track
    print(f'ASINs currently being tracked : {list_of_asins} \n')
    user_ans= str(input('Do you want to enter new ASINs to track reviews- yes or no : '))
    user_ans = user_ans.lower()  
    
    if user_ans == 'yes' or user_ans == 'no':
      break
    else:  
     print('Type either yes or no to Continue \n')  
  
  if user_ans == 'yes':
    print('Pass the ASIN of products you need to track the reviews \n')

    new_asin = str(input('Enter Asin : '))
    if new_asin in list_of_asins:
      print('ASIN already being tracked \n')
      user_input() # if we need to add different asin (recurssion)
  
      # there is an issue here if customer do not have any asin to add this might be infinite loop, i have intoduced break for that so it breaks from this while loop 
    else:
      list_of_asins.append(new_asin)
    


    user_continue = str(input('Do you need to enter more ASINs - yes or no : ' ))
    user_continue = user_continue.lower() 

    # if user types words otherthan yes or no
    while user_continue != 'no' and user_continue !='yes' :
      print('Enter either (yes/no) \n')
      user_continue = str(input('Do you need to enter more ASINs (yes or no) : ' ))
      user_continue = user_continue.lower()

    if user_continue =='no':  
      return list_of_asins

    elif user_continue =='yes':
      user_input()

    # if it is yes, the while loop runs again.  


  
  else:
    # list_of_asins = list(db['ASIN'])
    return list_of_asins

        
        
      
list_of_asins = user_input(db)      
  


# remove this code when you are using it in production, 
# this is just to make it easy to enter many asins at at time
# list_of_asins = ['B096FJG4FR', 'B08Y6PGH7S' ,'B08ZCP8DBS','B0957WJB9N','B07TM3LRVB',
                 # 'B08332221J','B07KYFHTGF','B08976V1BZ','B0849NLNTQ' ]
# list_of_asins = ['B07ZVXZNVD','B08Y6PGH7S']


db['ASIN'] = list_of_asins

print('processing... \n')

today = date.today()


list_of_reviews_per_asin = []
list_positive_reviews_per_asin =[]
title_of_products = []


web_url = 'https://www.amazon.in/dp/'


def browser(list_of_asins,web_url):

  while True:
    
    for asin in list_of_asins :
        
    
      new_url = web_url+ asin
      print(f'Checking the ratings of {asin} ... \n')
      driver.get(new_url)
      time.sleep(1)
      try: 
        driver.find_element_by_id('acrCustomerReviewText').click()
      except:
        print(f'There is an issue with {asin} Asin \n')
        list_of_reviews_per_asin.append('error with asin')
        list_positive_reviews_per_asin.append('error with asin')
        continue
    
      
      string_review = driver.find_element_by_id('acrCustomerReviewText').text
      total_ratings = string_review.split()[0]
      total_ratings = total_ratings.replace(',','')
      
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

      # finding title of products
      title_full = driver.find_element_by_id('productTitle').text
      title_as_list = title_full.split()


      title = title_as_list[0:4]
      title = ' '.join((title))
      title_of_products.append(title)
      
      time.sleep(1)
      
      
    
    
    today_neg = str(today) + '_neg'
    today_pos = str(today) + '_pos'
    db['Title']   = title_of_products
    db[today_neg] = list_of_reviews_per_asin
    db[today_pos] = list_positive_reviews_per_asin
    
    return db

def today_tracked(db): # function to see if the tracker was already ran today
  # we have to look into the case of tracking new asins in a day, then we have to run the function, but we do not need to do for those we have already done.
  
  values = db.prefix(str(today))
  if len(values) != 0:
    print('\nTracker already ran today \n')
    return db
  else:
    db = browser(list_of_asins,web_url)
    return db
    
db = today_tracked(db)
# db = browser(list_of_asins,web_url)
# db = browser(list_of_asins,web_url)



def create_table(db):
  dict = OrderedDict()

  for key in db.keys():
    dict[key]= list(db[key])

  print(tabulate(dict,headers='keys',tablefmt='fancy_grid')) 

  return dict # can be used to get csv file

create_table(db)

def delete_asin(db): # not done
  user_input_delete = str(input('\n Do you want to delete any asin from the table (yes/no) : '))
  user_input_delete = user_input_delete.lower() 

  while user_input_delete != 'no' and user_input_delete !='yes' :
    print('\n Enter either (yes/no)')
    user_input_delete = str(input('\n Do you want to delete any asin from the table (yes/no) : '))
    user_input_delete = user_input_delete.lower()

  if user_input_delete =='no':
    return None

  else:
    asin_input = str(input('\n Enter the Asin you want to delete : '))
    idx = db['ASIN'].index(asin_input)
    
    for key in db.keys():

      try:
        db[key].pop(idx)
        
      except:
        pass

    create_table(db)  # to show the asin is deleted 
  
delete_asin(db)    


def create_csv(db=db):
  
  csv_input = str(input('\n Do you want this file to be send as a CSV file to your email-id ? (yes/no) : '))

  if csv_input == 'yes' :

    dict_positive = {}
    dict_negative = {}
    for key in db.keys():
  
      if key.endswith('pos'):
    
        key_dic = key[:-4]
        dict_positive[key_dic] = db[key]

      elif key.endswith('neg'):

        key_dic = key[:-4]
        dict_negative[key_dic] = db[key]

    dict_negative['ASIN'] = db['ASIN']
    dict_negative['Title'] = db['Title']
  
    dict_positive['ASIN'] = db['ASIN']
    dict_positive['Title'] = db['Title']

    df_pos = pd.DataFrame.from_dict(dict_positive,orient='columns')
  
    df_pos.set_index(['ASIN','Title'],inplace= True)
    df_pos.to_csv('positive_review_data.csv')
  
    df_neg = pd.DataFrame.from_dict(dict_negative,orient='columns')
    df_neg.set_index(['ASIN','Title'],inplace= True)
    df_neg.to_csv('negative_review_data.csv')
  
    sent_email()
  
  elif csv_input == 'no':
    return None

  else:
    print('Enter either yes or no')
    create_csv()

  

create_csv(db)

driver.quit()