import unittest, requests, warnings, json, xmlrunner, datetime

warnings.filterwarnings('ignore')

class test_delete_rule(unittest.TestCase):
    
    def setUp(self):
        global condata, ruleId
        condata =['10.243.11.102', 'USERID', 'CME44ibm', '7C05E9DE339711E48EC9000AF74F19A4']
        #create Group
        data = {"description":"Todd_Test_Solution","members":["nodes/"+condata[3]],"name":"Todd_Test_Solution","solutionVPD":{"console":"https://192.0.2.0","id":"59A54997C18DCF0594B8AAAB","machineType":"8695","manufacturer":"Lenovo","model":"AC1","serialNumber":"103D4F44"},"type":"solution"}
        requests.post('https://'+condata[0]+'/resourceGroups',auth=(condata[1],condata[2]), verify=False, json = data)
        

                
        #create power state rule for power on
        data = {"content":["powerStatus=8"],"name":"powerRule","source":"server","targetGroups":["/resourceGroups/59A54997C18DCF0594B8AAAB"],"targetResourceType":[],"targetResources":[]}
        createRule = requests.post('https://'+condata[0]+'/compliance/rules', auth=(condata[1],condata[2]), verify=False, json=data)
        formatJson = json.loads(createRule.text)
        ruleId = formatJson[1]
        
    def test_001_delete_rule(self):
        test = requests.delete('https://'+condata[0]+'/compliance/rules/'+ruleId, auth=(condata[1],condata[2]), verify=False)
        formateJson = json.loads(str(test.text))
        self.assertEqual(test.status_code, 200, msg = 'Status code = '+str(test.status_code))
        self.assertEqual(formateJson[1], ruleId, msg='Rule Id does not match')
        self.assertEqual(formateJson[2],"successfully deleted", msg = 'Returned data = '+str(formateJson))
        

    
    def tearDown(self):
        requests.delete('https://'+condata[0]+'/resourceGroups/59A54997C18DCF0594B8AAAB', auth=(condata[1],condata[2]), verify=False)
            
        
    
if __name__=='__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='\\complaince_test_Reports_'+str(datetime.date.today())),failfast=False, buffer=False, catchbreak=False)
