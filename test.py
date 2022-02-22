from replit import db
import pandas as pd
from datetime import date
from datetime import timedelta


del db["2022-02-22neg"]
del db['2022-02-22pos']
print(db.keys())

print('done')