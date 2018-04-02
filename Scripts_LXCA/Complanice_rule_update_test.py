import unittest, requests, warnings, json, xmlrunner, datetime, random

warnings.filterwarnings('ignore')

class test_update_rule(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        global condata, serverList
        condata=['10.243.1.100', 'USERID', 'CME44len']
        serverList = inst.getUUIDlist(inst)
        condata =['10.243.1.100', 'USERID', 'CME44len', serverList[random.randint(0,len(serverList))]]
        #create Group
        data = {"description":"Test_Solution","members":["nodes/"+condata[3]],"name":"Test_Solution","solutionVPD":{"console":"https://192.0.2.0","id":"59A54997C18DCF0594B8AAAB","machineType":"8695","manufacturer":"Lenovo","model":"AC1","serialNumber":"103D4F44"},"type":"solution"}
        requests.post('https://'+condata[0]+'/resourceGroups',auth=(condata[1],condata[2]), verify=False, json = data)
        
        #Check power state of server and turn if needed
        check = requests.get('https://'+condata[0]+'/nodes/'+condata[3], verify = False, auth=(condata[1],condata[2]))
        formatJson = json.loads(str(check.text))
        powerState = formatJson['powerStatus']
        if powerState == 5:
            print('Power is off. Powering server on now')
            requests.put('https://'+condata[0]+'/nodes/'+condata[3]+'?synchronous=true',auth=(condata[1],condata[2]), verify=False, json = {"powerState":"powerOn"})
            time.sleep(5)
            count = 0
        
            while powerState != 8:
                check = requests.get('https://'+condata[0]+'/nodes/'+condata[3], verify = False, auth=(condata[1],condata[2]))
                formatJson = json.loads(str(check.text))
                powerState = formatJson['powerStatus']
                count = count + 1
                if powerState == 8:
                    print('The power is now on.')
                    time.sleep(5)
                time.sleep(5)
                if count >= 400:
                    print('Power state is ' +str(powerState)+ ' and could not be changed')
                    break
                
        #create power state rule for power on
        data = {"content":["powerStatus=8"],"name":"powerRule","source":"server","targetGroups":["resourceGroups/59A54997C18DCF0594B8AAAB"],"targetResourceType":["Server"],"targetResources":[]}
        createRule = requests.post('https://'+condata[0]+'/compliance/rules', auth=(condata[1],condata[2]), verify=False, json=data)
        formatJson = json.loads(createRule.text)
        i=formatJson['message']
        global ruleId
        ruleId = i[-24:]
        
    def test_001_update_rule(self):
        data = {"content":["powerStatus=5"],"name":"newPowerRule","source":"inventory","targetGroups":["resourceGroups/59A54997C18DCF0594B8AAAB"],"targetResourceType":["Server"],"targetResources":[]}
        updateRule = requests.put('https://'+condata[0]+'/compliance/rules/'+ ruleId, auth=(condata[1],condata[2]), verify=False, json=data)
        formatJson = json.loads(str(updateRule.text))
        self.assertEqual(updateRule.status_code, 200, msg = 'The state code was not 200 and instead was:'+str(updateRule.status_code))
        self.assertEqual(updateRule.json()[0]['content'][0], "powerStatus=5", msg = 'Rule content was not updated' )
        self.assertEqual(updateRule.json()[0]['name'], "newPowerRule", msg = 'Rule name was not updated' )
        
    def test_002_update_rule_result_check(self):
        data = {"solutionGroups":["59A54997C18DCF0594B8AAAB"]}
        test1 = requests.post('https://'+condata[0]+'/compliance/compositeResults/', auth=(condata[1],condata[2]), verify=False, json=data)
        resultsId = test1.json()['CompositeResults'][0]
        complianceCheck = requests.get('https://'+condata[0]+'/compliance/compositeResults/'+resultsId, auth=(condata[1],condata[2]), verify=False)
        formatJson = json.loads(str(complianceCheck.text))
        self.assertEqual(formatJson[0]['results'],False, msg='Results should be false. Please check to make sure nothing has powered the server off. Make sure the rule updated successfully in test_001')
            
    @classmethod        
    def tearDownClass(inst):
        requests.delete('https://'+condata[0]+'/compliance/rules/'+ruleId, auth=(condata[1],condata[2]), verify=False)
        requests.delete('https://'+condata[0]+'/resourceGroups/59A54997C18DCF0594B8AAAB', auth=(condata[1],condata[2]), verify=False)
            
            
    def powerCheck(self, condata):
        check = requests.get('https://'+condata[0]+'/nodes/'+condata[3], verify = False, auth=(condata[1],condata[2]))
        formatJson = json.loads(str(check.text))
        powerState = formatJson['powerStatus']
        return powerState
    
    def getUUIDlist(self):
        uuidlist =[]
        invlist = requests.get('https://'+condata[0]+'/nodes', auth=(condata[1],condata[2]), verify=False)
        invlist1 =json.loads(str(invlist.text))
        for items in invlist1['nodeList']:
            if items['status']['name'] == 'MANAGED':
                uuidlist.append(items['uuid'])
        return uuidlist   
    
if __name__=='__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='\\complaince_test_Reports_'+str(datetime.date.today())),failfast=False, buffer=False, catchbreak=False)


        
        
    
