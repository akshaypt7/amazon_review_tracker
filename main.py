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



# print(f'db.  {db}')

list_of_asins = list(db['ASIN']) # we access the old ASINs

def user_input(db=db):

  '''Here we ask for the input from the user to add new asins to track. We also display the ASINS we are tracking.'''

  while True:

    print(f'Asins Currently being tracked : {list_of_asins}  .')
    user_ans= str(input('Do you want to enter new ASINs to track reviews- yes or no : '))
    user_ans = user_ans.lower()  
    
    if user_ans != 'yes' and user_ans != 'no':
      print('Type either yes or no to Continue \n') 
      continue
  
    elif user_ans == 'yes':
      print('Pass the ASIN of products you need to track the reviews \n')
    
      new_asin = str(input('Enter Asin : '))
      
      if new_asin in list_of_asins:
        print('ASIN already being tracked \n')
        # user_input() # if we need to add different asin (recurssion)
        continue
      else:
        list_of_asins.append(new_asin)
        continue
        
        # there is an issue here if customer do not have any asin to add this might be infinite loop, i have intoduced break for that so it breaks from this while loop 
    elif user_ans == 'no':
      # list_of_asins.append(new_asin)
      return list_of_asins


      
list_of_asins = user_input(db)       # new updated list of asins
  


# remove this code when you are using it in production, 
# this is just to make it easy to enter many asins at at time
# list_of_asins = ['B096FJG4FR', 'B08Y6PGH7S' ,'B08ZCP8DBS','B0957WJB9N','B07TM3LRVB',
                 # 'B08332221J','B07KYFHTGF','B08976V1BZ','B0849NLNTQ' ]
# list_of_asins = ['B07ZVXZNVD','B08Y6PGH7S']


db['ASIN'] = list_of_asins # writing the new asins we added back into the database

print('processing... \n')

today = date.today()


list_of_reviews_per_asin = []
list_positive_reviews_per_asin =[]
title_of_products = []


web_url = 'https://www.amazon.in/dp/'


def browser(list_of_asins,web_url):

  '''Here we use selenium to browse through each product in amzon using its ASIN, and we calcualte the postive and negative reviews we received for each product'''

  while True:
    
    for asin in db['ASIN'] :
        
    
      new_url = web_url+ asin
      print(f'Checking the ratings of {asin} ... \n')
      driver.get(new_url)
      time.sleep(1)
      try: 
        driver.find_element_by_id('acrCustomerReviewText').click() # finding the reviews
      except:
        print(f'There is an issue with {asin} Asin \n')
        list_of_reviews_per_asin.append('error with asin')
        list_positive_reviews_per_asin.append('error with asin')
        continue
    
      
      string_review = driver.find_element_by_id('acrCustomerReviewText').text # getting the total ratings
      total_ratings = string_review.split()[0] # converting to integer
      total_ratings = total_ratings.replace(',','')
      
      total_ratings = int(total_ratings)
    
    # finding the positive and negative ratings of each product
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

      # finding title of each product
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

#If the tracker already ran today this function asks if we need to run it again incase if we added new products

  values = db.prefix(str(today))
  if len(values) != 0:
    print('Tracker already ran today\n')
    user_input = str(input('Do you want to run it again(yes/no): '))
    if user_input== 'yes':
      
      db = browser(list_of_asins,web_url)
      return db
    elif user_input =='no':
      return db
    else:
      today_tracked(db)
    
  else:
    db = browser(list_of_asins,web_url)
    return db
    
db = today_tracked(db)


def create_table(db):
  dict = OrderedDict()

  for key in db.keys():
    dict[key]= list(db[key])

  print(tabulate(dict,headers='keys',tablefmt='fancy_grid')) 

  return dict # can be used to get csv file

create_table(db)

def delete_asin(db): # 
  """If we need to delete any asins we have entered we can use this function"""

  
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

# This function create csv file of the database and sends its as email
# We use another function from email_csv for sending the email.
  
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

    
    df_pos = pd.DataFrame.from_dict(dict_positive,orient='index').T
    df_pos.sort_index(axis=1,inplace=True)
    df_pos.set_index(['ASIN','Title'],inplace= True)

    
    df_pos.to_csv('positive_review_data.csv')
  
    df_neg = pd.DataFrame.from_dict(dict_negative,orient='index').T # there wont be any issues with arrays of different length, this happens when we add new asin, as some of the cells will be empty.
    df_neg.sort_index(axis=1,inplace=True) # to have the columns in ascending order
    df_neg.set_index(['ASIN','Title'],inplace= True)
    df_neg.to_csv('negative_review_data.csv')

    # Calling the function from email_csv to send email
    sent_email()
  
  elif csv_input == 'no':
    return None

  else:
    print('Enter either yes or no')
    create_csv()

  

create_csv(db)

driver.quit()