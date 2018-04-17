import requests, warnings
warnings.filterwarnings('ignore')
global key, bz
key='AirXEelVqsNtHp4I3OwavnZpVBcG5OdaKf8zuU0S'
bz='https://bz.labs.lenovo.com'

def getBugList():
    fullBugList =[]
    search=requests.get(bz+'/rest/bug?bug_status=Open&bug_status=Working&bug_status=Rejected&product=CMM&product=DSA&product=LXCE_BoMC&product=LXCE_OneCLI&product=LXCE_UpdateXpress&product=LXCI&product=SCOM&product=SCVMM&product=XClarity%20Administrator&resolution=---&api_key='+key,verify=False)
    for bug in search.json()['bugs']:
        fullBugList.append(bug['id'])
        
    
    return fullBugList

def checkBugHistory(buglist):
    rejCount = 0
    suspectBugList=[]
    for bug in buglist:
        print('******************Checking Bug #'+str(bug)+' now!****************************')
        search=requests.get(bz+'/rest/bug/'+str(bug)+'/history?&api_key='+key,verify=False)
        for change in search.json()['bugs'][0]['history']:
            for r in change['changes']:
                if r['field_name'] == 'status' and r['added'] == 'Rejected':
                    print('     Feid name is '+r['field_name'] + ' and '+r['added']+' was added')
                    rejCount = rejCount + 1
                    print('    Count is '+str(rejCount))
                    if rejCount >2:
                        suspectBugList.append(bug)
                        rejCount = 0
                        print('        '+str(rejCount)+ ' should be Zero now')
        print('*****Done with Bug# '+str(bug)+' counter is '+str(rejCount)+' Setting counter back to zero now*****')
        rejCount = 0
                        
    return suspectBugList
                        
                
                

list1 = getBugList()
badBuglist = checkBugHistory(list1)
print(badBuglist)