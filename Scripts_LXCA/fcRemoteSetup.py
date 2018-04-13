#! python3
import json
import requests
import sys
import warnings

warnings.filterwarnings('ignore')
#condata = ['10.243.1.90','CME44len']

lxcaip = sys.argv[1]
user = sys.argv[2]
pw = sys.argv[3]

def setupremoteserver(lxcaip, user, pw):
        print('Setting up remote image server now.')
        payload = {"address":"10.243.1.98","displayName":"Flexcat Image Server","password":"CME44len","port":80,"protocol":"HTTP","username":"FTP"}
        remoteserver = requests.post('https://'+lxcaip+'/osImages/remoteFileServers', auth=(user,pw), verify=False, json=payload)
        remoteserver1 = json.loads(str(remoteserver.text))
        print('Set Remote Server '+ (str(remoteserver)))
        print(remoteserver1['result'])
        return remoteserver


        
#setglobal(condata)
chck = setupremoteserver(lxcaip,user,pw)
print(chck.status_code)
