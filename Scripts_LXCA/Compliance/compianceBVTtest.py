import requests, sys, warnings
warnings.filterwarnings('ignore')

global lxcaip, usernm, PASSWD

lxcaip = '10.243.1.100'
usernm = 'USERID'
passwd = 'CME44len'


def getuuid():
    global uuid
    uuidlist =[]
    try:
        invlist = requests.get('https://'+lxcaip+'/nodes', auth=(usernm,passwd), verify=False)
    except requests.exceptions.ConnectionError:
        sys.exit('Unable to connect to LXCA')
    for items in invlist.json()['nodeList']:
        if items['status']['name'] == 'MANAGED':
            uuidlist.append(items['uuid'])
    try:
        uuid = uuidlist[0]
        
    except IndexError:
        sys.exit("Not Tested, no device found")
        
mainStatus = True    

#Create a resource group using any server it doesn't matter which one
def main():
    data = {"description":"Test_Solution","members":["nodes/"+uuid],"name":"Test_Solution","solutionVPD":{"console":"https://192.0.2.0","id":"59A54997C18DCF0594B8CCCC","machineType":"8695","manufacturer":"Lenovo","model":"AC1","serialNumber":"103D4F44"},"type":"solution"}
    createGroup = requests.post('https://'+lxcaip+'/resourceGroups',auth=(usernm,passwd), verify=False, json = data)
    if createGroup.status_code != 200:
        mainStatus = False
        
#Create a rule for the group

    data = {"content":["uuid="+uuid],"name":"ruleCheckUUID","source":"inventory","targetGroups":["resourceGroups/59A54997C18DCF0594B8CCCC"],"targetResourceType":["server"],"targetResources":[]}
    createRule = requests.post('https://'+lxcaip+'/compliance/rules', auth=(usernm,passwd), verify=False, json=data)
    if createRule.status_code != 201:
        mainStatus = False
#Check rule

    data = {"solutionGroups":["59A54997C18DCF0594B8CCCC"]}
    compositeResultes = requests.post('https://'+lxcaip+'/compliance/compositeResults/', auth=(usernm,passwd), verify=False, json=data)
    if compositeResultes.status_code != 200:
        mainStatus = False

    if mainStatus == True:
        return True
    else:
        return False

getuuid()





if __name__ == "__main__":
    if main() == True:
        print ("")
        print ("+++++++++++++++++++++++++++++++++++++++++++")
        print ("+++ Integration Compliance Test Passed  +++")
        print ("+++++++++++++++++++++++++++++++++++++++++++")
        '''try:
            Logout_process()
        except:
            pass'''
        # mydriver.quit()
        sys.exit("Passed")
    else:
        print ("Integration Compliance Test Failed")
        '''try:
            Logout_process()
        except:
            pass'''
        #mydriver.quit()
        sys.exit("Failed") 


