import requests
import re
import json
import os
import urllib3
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FQDN="x.x.x.x"
userurlbase = "https://"+FQDN+"/api/guest/username/"
tableurl = "https://"+FQDN+"/api/guest?filter=%7B%7D&sort=-id&offset=0&limit=1000&calculate_count=false"


with open('/root/token.json','r') as f:
    data=json.load(f)
    access_token=data['access_token']

print(datetime.now())

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer "+access_token
}

try:
    r = requests.get(tableurl, headers=headers,verify=False)
    usertable = json.loads(r.text)
except Exception as e:
    print(e)
    exit(1)

for data in usertable['_embedded']['items']:
    d_username=data['username']
    d_enabled=data['enabled']
    d_mac=data['mac']
    d_ap=data['apname']
    d_ip=data['remote_addr']
    #print(d_username,d_enabled)
    try:
        errorflag=0
        emailObject =validate_email(d_username)
    except EmailNotValidError as errorMsg:
        if d_enabled:
            print(str(errorMsg),d_username,d_enabled,d_mac,d_ap,d_ip)
        errorflag=1
    if errorflag:
        try:
            if d_enabled:
                headers = {'Authorization':'Bearer '+access_token,'Accept':'application/json','Content-Type':'application/json'}
                data = {"enabled":False}
                url = userurlbase + requests.utils.quote(d_username)
                print("url:",url)
                response=requests.patch(url,headers=headers,json=data,verify=False)
                print(response)
        except Exception as e:
            print(e)
