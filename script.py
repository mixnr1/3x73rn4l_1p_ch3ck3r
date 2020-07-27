import os
import requests
import config
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendnewip(ipaddr):
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    password = config.password
    message = MIMEMultipart("alternative")
    timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
    message["Subject"] = "IP Address Change "+timestr 
    message["From"] = sender_email
    message["To"] = receiver_email
    plain = "New external IP address is: " + str(ipaddr)
    part1 = MIMEText(plain, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def updateipstore(ipaddr, ipstorepath):
    currentip = open(ipstorepath, 'w')
    currentip.write(ipaddr)
    currentip.truncate()
    currentip.close()

try:
    import urllib3
    urllib3.disable_warnings()
    ipaddr = requests.get("https://api.ipify.org", verify=False, timeout=10).text
    if os.path.isfile(config.ipstorepath): 
        currentip = open(config.ipstorepath, 'r+') 
        if currentip.read() != ipaddr: 
            currentip.close()
            updateipstore(ipaddr, config.ipstorepath)
            sendnewip(ipaddr) 
    else: 
        updateipstore(ipaddr, config.ipstorepath) 
except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
    pass
