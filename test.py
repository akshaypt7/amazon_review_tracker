from replit import db
import pandas as pd
from datetime import date
from datetime import timedelta
from tabulate import tabulate


# del db["2022-02-22neg"]
# del db['2022-02-22pos']
# print(db.keys())
# from collections import OrderedDict

# db.clear()

idx = db['ASIN'].index('B09RSS8BTV')
print(idx)
print(db.iloc[idx])

print('done')