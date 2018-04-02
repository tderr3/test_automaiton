import unittest, requests, warnings, json, time, xmlrunner, datetime, random





class testRulesPOST(unittest.TestCase):
    warnings.filterwarnings('ignore')
    @classmethod
    def setUpClass(inst):
        global condata, serverList
        condata=['10.243.1.100', 'USERID', 'CME44len']
        serverList = inst.getUUIDlist(inst)
        condata =['10.243.1.100', 'USERID', 'CME44len', serverList[random.randint(0,len(serverList))]]
        data = {"description":"Test_Solution","members":["nodes/"+condata[3]],"name":"Test_Solution","solutionVPD":{"console":"https://192.0.2.0","id":"59A54997C18DCF0594B8AAAB","machineType":"8695","manufacturer":"Lenovo","model":"AC1","serialNumber":"103D4F44"},"type":"solution"}
        requests.post('https://'+condata[0]+'/resourceGroups',auth=(condata[1],condata[2]), verify=False, json = data)
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
    
        
        
        
    def test_001_POST_rule(self):
        global ruleId
        data = {"content":["powerStatus=8"],"name":"powerRule","source":"inventory","targetGroups":["resourceGroups/59A54997C18DCF0594B8AAAB"],"targetResourceType":["Server"],"targetResources":[]}
        createRule = requests.post('https://'+condata[0]+'/compliance/rules', auth=(condata[1],condata[2]), verify=False, json=data)
        formatJson = json.loads(createRule.text)
        #self.assertEqual(formatJson[0], "Rule successfully created and stored against id:")
        self.assertEqual(createRule.status_code, 201)
        i=formatJson['message']
        ruleId = i[-24:]
        time.sleep(10)
        
    
    def test002POSTcompositeResultcheck(self):
        print('Generataing Composite Results')
        data = {"solutionGroups":["59A54997C18DCF0594B8AAAB"]}
        test1 = requests.post('https://'+condata[0]+'/compliance/compositeResults/', auth=(condata[1],condata[2]), verify=False, json=data)
        self.assertEqual(test1.status_code, 200)
        resultsId = test1.json()['CompositeResults'][0]
        print(resultsId)
        time.sleep(10)
        complianceCheck = requests.get('https://'+condata[0]+'/compliance/compositeResults/'+resultsId, auth=(condata[1],condata[2]), verify=False)
        formatJson = json.loads(str(complianceCheck.text))
        print(formatJson[0]['results'])
        print('The reslults are '+str(formatJson[0]['results']))
        self.assertEqual(formatJson[0]['results'],True, msg='Results should be true. Please check to make sure nothing has powered the server off')
        
        
    def test003compositeReslultsFail(self):
        powerState = self.powerCheck(condata)
        if powerState == 8:
            print('Power is on. Powering server off now')
            requests.put('https://'+condata[0]+'/nodes/'+condata[3]+'?synchronous=true',auth=(condata[1],condata[2]), verify=False, json = {"powerState":"powerOff"})
            time.sleep(5)
            count = 0
        
            while powerState != 5:
                powerState = self.powerCheck(condata)
                count = count + 1
                time.sleep(5)
                if powerState == 5:
                    print('The power is now on.')
                    time.sleep(5)
                if count >= 400:
                    print('Power state is ' +str(powerState)+ ' and could not be changed')
                    break
            
            
            
        data = {"solutionGroups":["59A54997C18DCF0594B8AAAB"]}
        test1 = requests.post('https://'+condata[0]+'/compliance/compositeResults/', auth=(condata[1],condata[2]), verify=False, json=data)
        resultsId = test1.json()['CompositeResults'][0]
        #formatJson = json.loads(str(test1.text))
        #resultsId = formatJson[1][0]
        print(resultsId)
        time.sleep(10)
        complianceCheck = requests.get('https://'+condata[0]+'/compliance/compositeResults/'+resultsId, auth=(condata[1],condata[2]), verify=False)
        formatJson = json.loads(str(complianceCheck.text))
        print(formatJson[0]['results'])
        self.assertEqual(formatJson[0]['results'],False, msg='Results should be false. Please check to make sure nothing has powered the server on')
        
        
        
        
    def test004POSTsecondRule(self):
        global ruleId2
        data = {"content":["name='Bonneville_FC'"],"name":"NameRule","source":"inventory","targetGroups":["resourceGroups/59A54997C18DCF0594B8AAAB"],"targetResourceType":["Server"],"targetResources":[]}
        createRule = requests.post('https://'+condata[0]+'/compliance/rules', auth=(condata[1],condata[2]), verify=False, json=data)
        formatJson = json.loads(createRule.text)
        #self.assertEqual(formatJson[0], "Rule successfully created and stored against id:")
        self.assertEqual(createRule.status_code, 201)
        i=formatJson['message']
        ruleId2 = i[-24:]
        time.sleep(10)
    
    def testscript(self):
        print(serverList)
    
    
    
    
        
    @classmethod
    def tearDownClass(inst):
        #global ruleId
        rules = requests.get('https://'+condata[0]+'/compliance/rules/', auth=(condata[1],condata[2]), verify=False)
        for i in rules.json():
            requests.delete('https://10.243.1.100/compliance/rules/'+i['id'],auth=(condata[1],condata[2]), verify=False)
        #requests.delete('https://'+condata[0]+'/compliance/rules/'+ruleId, auth=(condata[1],condata[2]), verify=False)
        #requests.delete('https://'+condata[0]+'/compliance/rules/'+ruleId2, auth=(condata[1],condata[2]), verify=False)
        requests.delete('https://'+condata[0]+'/resourceGroups/59A54997C18DCF0594B8AAAB', auth=(condata[1],condata[2]), verify=False)
        #unittest.TestCase.tearDown(self)
        
    
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
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='c:\\pydata\\complaince_test_Reports_'+str(datetime.date.today())),failfast=False, buffer=False, catchbreak=False)
