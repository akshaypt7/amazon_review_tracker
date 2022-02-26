from replit import db
import pandas as pd
from datetime import date
from datetime import timedelta
from tabulate import tabulate

import os
# del db["2022-02-22neg"]
# del db['2022-02-22pos']
# print(db.keys())
from collections import OrderedDict

# db.clear()

# my_secret = os.getenv['email_username']
my_secret = os.environ['email_username']
print(os.getenv("email_username"))
print(my_secret)
# idx = db['ASIN'].index('B09RSS8BTV')
# print(db.keys())
# # print(idx)
# # # print(db.iloc[idx])
# # print('---')
# print(db['ASIN'])
# print('---')
# print(db['ASIN'].pop(1))
# print('---')
# print(db['ASIN'])


# dict = OrderedDict()

# for key in db.keys():
#   dict[key]= list(db[key])


# print(dict)
# print('--')
# df = pd.DataFrame(dict, columns = dict.keys())
# print(df)
# print('--')
# df.to_csv('review_data.csv', index=False)

print('done')
