from replit import db
import pandas as pd
# from datetime import date
# from datetime import timedelta
# from tabulate import tabulate

# import os
# # del db["2022-02-22neg"]
# # del db['2022-02-22pos']
# # print(db.keys())
# from collections import OrderedDict

# db.clear()

# my_secret = os.getenv['email_username']
# my_secret = os.environ['email_username']
# print(os.getenv("email_username"))
# print(my_secret)
# idx = db['ASIN'].index('B09RSS8BTV')
# print(db.keys())
# # print(idx)
# # # print(db.iloc[idx])
# # print('---')

# print('---')
# print(db['ASIN'].pop(1))
# print('---')

# values = db.prefix(str(today))


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


# df = pd.DataFrame.from_dict(dict_positive,orient='columns')
# df.set_index(['ASIN','Title'],inplace= True)
# print(df)
df_pos = pd.DataFrame.from_dict(dict_positive,orient='columns')

df_pos.set_index(['ASIN','Title'],inplace= True)
df_pos.to_csv('positive_review_data.csv')

df_neg = pd.DataFrame.from_dict(dict_negative,orient='columns')
df_neg.set_index(['ASIN','Title'],inplace= True)
df_neg.to_csv('negative_review_data.csv')

# with pd.ExcelWriter('output.xlsx') as writer:
#     df_pos.to_excel(writer, sheet_name='positive')
#     df_neg.to_excel(writer, sheet_name='negative')

# read_file = pd.read_excel("output.xlsx")
  
# Write the dataframe object
# into csv file


print('done')

