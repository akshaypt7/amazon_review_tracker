import os
import smtplib


# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
s.starttls()
  
# Authentication
secret_email = os.environ['email_username']
email_password = os.environ['email_password']
s.login(secret_email, email_password)


  
# message to be sent
message = "first automated mail from me"


# sending the mail
s.sendmail(secret_email, "natid85881@spruzme.com", message)

print('done')
# terminating the session
s.quit()



# resources 
# http://blog.magiksys.net/generate-and-send-mail-with-python-tutorial 
# https://stackoverflow.com/questions/38825943/mimemultipart-mimetext-mimebase-and-payloads-for-sending-email-with-file-atta