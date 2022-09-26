from imap_tools import MailBox, AND
import requests
import re
import json
import os
import urllib3
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FQDN="x.x.x.x"
userurlbase = "https://"+FQDN+"/api/guest/username/"
SECRET="key"
cuser="username"
cpassword='password'
user = "email address"
password = "email password

with open('/root/token.json','r') as f:
    data=json.load(f)
    access_token=data['access_token']

try:
    mb = MailBox('imap.gmail.com').login(user, password,initial_folder='2_NDR')
    messages = mb.fetch(criteria=AND(seen=False),mark_seen=True,bulk=True)
except Exception as e:
    print(e)
    exit(1)

#print(access_token)
for msg in messages:
    #print(msg.text)
    print(msg.date_str)
    emailname=re.findall(r" delivered to (.*?) because",msg.text)
    if emailname:
        try:
            print(emailname[0])
            headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','Content-Type':'application/json'}
            data = {"enabled":False}
            url = userurlbase + requests.utils.quote(emailname[0])
            print(url)
            response=requests.patch(url,headers=headers,json=data,verify=False)
            print(response)
        except Exception as e:
            print(e)
            exit(1)
