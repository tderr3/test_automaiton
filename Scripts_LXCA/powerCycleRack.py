import json, requests, time, warnings, datetime, sys

warnings.filterwarnings('ignore')

lxcaip = sys.argv[0]
userid = sys.argv[1]
passwd = sys.argv[2]

x = 0
#count = int(sys.argv[4])
count = 10

def getUUIDlist(lxcaip, userid, passwd):
    uuidlist =[]
    invlist = requests.get('https://'+lxcaip+'/nodes', auth=(userid,passwd), verify=False)
    invlist1 =json.loads(str(invlist.text))
    for items in invlist1['nodeList']:
        if items['type'] == 'Rack-Tower Server' and items['status']['name'] == 'MANAGED':
            uuidlist.append(items['uuid'])
        elif items['type'] == 'NeXtScale' and items['status']['name'] == 'MANAGED':
            uuidlist.append(items['uuid'])            
    return uuidlist

def updatePowerState(lxcaip, userid, passwd, uuidlist):
    for server in uuidlist:
        powerstate = requests.get('https://'+lxcaip+'/nodes/'+server, auth=(userid,passwd), verify=False)
        powerstate1 = json.loads(str(powerstate.text))
        if powerstate1['powerStatus'] == 8:
            print('Server '+server+' powerstate is on turning off now')
            data = {"powerState": "powerOff"}
            requests.put('https://'+lxcaip+'/nodes/'+server, auth=(userid,passwd), verify=False, json=data)
            time.sleep(10)
        elif powerstate1['powerStatus'] == 5:
            print('Server '+server+' powerstate is off no setup action needed')
        elif powerstate1['powerStatus'] == 0:
            print('Server '+server+' powerstate is unknown and may need to be checked manually')

def powerOnServers(lxcaip, userid, passwd, uuidlist):
    on = {"powerState": "powerOn"}
    for server in uuidlist:
        power = requests.put('https://'+lxcaip+'/nodes/'+server, auth=(userid,passwd), verify=False, json=on)
        if str(power) == '<Response [200]>':
            print('Server '+server+' power on command successful')
        else:
            print('Server '+server+' power on command failed')
        time.sleep(60)
        check = powerStateCheck(lxcaip, userid, passwd, server)
        if check == 8:
            print('Test on '+server+': Successful')
        else:
            print('Test on '+server+': Failed! State: '+str(check)+' Time: '+str(datetime.datetime.now()))
    
def powerOffServers(lxcaip,userid, passwd, uuidlist):
    off = {"powerState": "powerOff"}
    for server in uuidlist:
        power = requests.put('https://'+lxcaip+'/nodes/'+server, auth=(userid,passwd), verify=False, json=off)
        if str(power) == '<Response [200]>':
            print('Server '+server+' power off command successful')
        else:
            print('Server '+server+' power off command failed')
        time.sleep(60)
        check = powerStateCheck(lxcaip, userid, passwd, server)
        if check == 5:
            print('Test:off '+server+': Successful')
        else:
            print('Test off '+server+': Failed! State: '+str(check)+' Time: '+str(datetime.datetime.now()))
        
def powerStateCheck(lxcaip, userid, passwd, uuid):
    powerstate = requests.get('https://'+lxcaip+'/nodes/'+uuid, auth=(userid,passwd), verify=False)
    powerstate1 = json.loads(str(powerstate.text))
    state = powerstate1['powerStatus']
    return state
           

uuidlist = getUUIDlist(lxcaip, userid, passwd)
updatePowerState(lxcaip, userid, passwd, uuidlist)
time.sleep(25)

while x <= count: 
    powerOnServers(lxcaip, userid, passwd, uuidlist)
    time.sleep(30)
    powerOffServers(lxcaip, userid, passwd, uuidlist)
    time.sleep(30)
    x + 1

print('Done')
            
            
