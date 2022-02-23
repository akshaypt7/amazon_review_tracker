from replit import db
import pandas as pd
from datetime import date
from datetime import timedelta
from tabulate import tabulate


# del db["2022-02-22neg"]
# del db['2022-02-22pos']
# print(db.keys())
from collections import OrderedDict

dict = OrderedDict()

for key in db.keys():
  dict[key]= list(db[key])

print(tabulate(dict,headers='keys',tablefmt='fancy_grid'))

print('done')