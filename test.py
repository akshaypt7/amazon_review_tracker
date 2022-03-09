from replit import db
import pandas as pd
# from datetime import date
# from datetime import timedelta
# from tabulate import tabulate

import os
import flask
import requests


# print(os.getenv("REPLIT_DB_URL"))
db_url =os.getenv("REPLIT_DB_URL")

app = flask.Flask(__name__)
sess = requests.Session()

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "DELETE"])
def proxy(path):
  url = os.environ["REPLIT_DB_URL"]
  if flask.request.path != "/":
    url += flask.request.path

  req = requests.Request(flask.request.method, url, data=flask.request.form, params=flask.request.args).prepare()
  resp = sess.send(req)

  proxy_resp = flask.make_response(resp.text)
  proxy_resp.status_code = resp.status_code
  for k, v in resp.headers.items():
    proxy_resp.headers[k] = v

  return proxy_resp


new_db = proxy(db_url)
print(new_db.keys())
  




print('done')

