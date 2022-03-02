import smtplib

from email.mime.multipart import MIMEMultipart
# from email.mime.mimetext import MIMEText
from email.mime.base import MIMEBase
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText

# from email.MIMEBase import MIMEBase
from email import encoders
import os

def sent_email():
  
  secret_email = os.environ['email_username']
  email_password = os.environ['email_password']
  
  fromaddr = secret_email
  
  toaddr = str(input('\n Enter your email-id : '))
  # toaddr = "akshayranjith1693@gmail.com" 
  password = email_password
  
  msg = MIMEMultipart()
  
  msg['From'] = fromaddr
  msg['To'] = toaddr
  msg['Subject'] = "Amazon Ratings Report "
  
  body = "Please find the document"
  
  msg.attach(MIMEText(body, 'plain'))
  
  filename = "positive_review_data.csv"
  attachment = open("positive_review_data.csv", "rb")
  
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  
  msg.attach(part)

# second csv

  filename_2 = "negative_review_data.csv"
  attachment_2 = open("negative_review_data.csv", "rb")
  
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment_2).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', "attachment; filename= %s" % filename_2)
  
  msg.attach(part)
  
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(fromaddr, password)
  text = msg.as_string()
  try :
    server.sendmail(fromaddr, toaddr, text)
    print('Email Sent')
  except:
    print('There was an Error sending the mail to your address (please check your email address)')
    
    email_input = str(input('Do you want to try again (yes/no): '))
    if email_input == 'yes':
      sent_email()
    else:
      return None
  server.quit()
