
import time
import cv2
import numpy as np

## SEND EMAIL ALERTS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
#from sinchsms import SinchSMS
# import msg91_sms as msgsms


# def email_alert(name, rtsp, reason):
#     print('sending email alert')
#     sender = "artificialintelligenceeco@yahoo.com"
#     #receiver = ["rishabh@omnipresenttech.com", "prosenjita@gmail.com"]
#     #receiver = "prosenjita@gmail.com"
#     receiver = "rishabh@omnipresenttech.com"
#     msg = MIMEMultipart()
#     msg['From'] = "omnipresent"
#     msg['to'] = receiver
#     msg['Subject'] = "[	ATTENTION USER	]"
#     t = time.localtime()
#     currentTime = time.strftime("%H:%M:%S", t)
#     body = " Camera: '{} 'has encountered Trespass event at {}".format(name,str(currentTime))
#     msg.attach(MIMEText(body, 'plain'))

#     #try:
#     # creates SMTP session
#     s = smtplib.SMTP("smtp.mail.yahoo.com",587)
#     # start TLS for security
#     s.starttls()
#     # Authentication
#     s.login(sender, "2a4rjz4JSk7NKYa")
#     #print("Logging into server account")

#     # Converts the Multipart msg into a string
#     text = msg.as_string()
#     #for i in receiver:
#    # 	print(i)
#     s.sendmail(sender, receiver, text)
#     # terminating the session
#     s.quit()
#     #except:
#     #    print("Email not sent, No Internet Connection")
#     #    pass


## Mohak refer to this code for SMS

def sendSMS(message):
    try:

        msg = msgsms.Cspd_msg91(apikey='284542AtO46RNh5d257617')
        sender = "omniLC"
        #phone_number = '918017637753','919163921332'
        #phone_number = '919933504113'
        phone_number = '918017637753','919831797256'
        SMS_text = message
        send_sms_resp = msg.send(4,sender,phone_number,SMS_text)
        print(send_sms_resp)
    except:
        pass

#sendSMS("hello_test")
