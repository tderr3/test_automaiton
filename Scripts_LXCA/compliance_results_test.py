import unittest, requests, warnings, json, xmlrunner, datetime, random
#Lxca setup
#Chassis or servers managed

warnings.filterwarnings('ignore')

class test_update_rule(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        global condata, serverList
        condata=['10.243.1.100', 'USERID', 'CME44len']
        serverList = inst.getUUIDlist(inst)
            
        try:
            condata =['10.243.1.100', 'USERID', 'CME44len', serverList[random.randint(0,len(serverList))], serverList[random.randint(0,len(serverList))]]
            while condata[3] == condata[4]:
                condata.remove(condata[4])
                condata.append(serverList[random.randint(0,len(serverList))])
        except:
            condata =['10.243.1.100', 'USERID', 'CME44len', serverList[random.randint(0,len(serverList))], serverList[random.randint(0,len(serverList))]]
            while condata[3] == condata[4]:
                condata.remove(condata[4])
                condata.append(serverList[random.randint(0,len(serverList))])
        #create Group
        data = {"description":"Test_Solution_multiNode","members":["nodes/"+condata[3],"nodes/"+condata[4]],"name":"Test_Solution_multiNode","solutionVPD":{"console":"https://192.0.2.0","id":"59A54997C18DCF0594B8AAAC","machineType":"8695","manufacturer":"Lenovo","model":"AC1","serialNumber":"103D4F44"},"type":"solution"}
        requests.post('https://'+condata[0]+'/resourceGroups',auth=(condata[1],condata[2]), verify=False, json = data)
        

        #create power state rule for power on
        data = {"content":["powerStatus=8"],"name":"powerRule","source":"inventory","targetGroups":["resourceGroups/59A54997C18DCF0594B8AAAC"],"targetResourceType":["server"],"targetResources":[]}
        createRule = requests.post('https://'+condata[0]+'/compliance/rules', auth=(condata[1],condata[2]), verify=False, json=data)
        formatJson = json.loads(createRule.text)
        global ruleId
        ruleId=formatJson['id']
        
        #ruleId = i[]
        
        data = {"solutionGroups":["59A54997C18DCF0594B8AAAC"]}
        test1 = requests.post('https://'+condata[0]+'/compliance/compositeResults/', auth=(condata[1],condata[2]), verify=False, json=data)
        global resultsId
        resultsId = test1.json()[0][0]['id']

        
        
    def test_001_check_results_for_compositeResult(self):
        test = requests.get('https://'+condata[0]+'/compliance/compositeResults/'+resultsId, auth=(condata[1],condata[2]), verify=False)
        results = test.json()['complianceResults']
        self.assertEqual(len(results), 2)

        
    #def test_002_update_rule_result_check(self):
        
            
    @classmethod        
    def tearDownClass(inst):
        requests.delete('https://'+condata[0]+'/compliance/rules/'+ruleId, auth=(condata[1],condata[2]), verify=False)
        requests.delete('https://'+condata[0]+'/resourceGroups/59A54997C18DCF0594B8AAAC', auth=(condata[1],condata[2]), verify=False)
        return None    
            
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


        
        
    
