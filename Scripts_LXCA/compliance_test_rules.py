import unittest, requests, warnings, json

warnings.filterwarnings('ignore')

class testRulesPOST(unittest.TestCase):
    def setUp(self):
        requests.get('https://10.243.5.200/compliance/rules',auth=('guest','CME44len'), verify=False)
        
    def test001POSTrule(self):
        data = {"name":"testRule","targetGroup":"/groups/59A54997C18DCF0594B8CCD5","targetResourceType":["Switch"],"content":[{"property":"powerState","ref_value":"On","source":"inventory"}]}
        test = requests.post('https://10.243.5.200/compliance/rules', auth=('guest','CME44len'), verify=False, json=data)
        t = json.loads(test.text)
        self.assertEqual(t[0], "Rule successfully created.")
        #self.assertEqual(t[2], "5a79f05d421aa910acf0cc73")
        self.assertEqual(test.status_code, 200)
        self.ruleId = t[2]
    
    def test002DeleteRule(self):
        test = requests.delete('https://10.243.5.200/compliance/rules/'+ self.ruleId , auth=('guest','CME44len'), verify=False)
        t = json.loads(test.text)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(t[1],self.ruleId)
        self.assertEqual(t[2], "successfully deleted")
    
    
    def tearDown(self):
        
        unittest.TestCase.tearDown(self)
        
        
if __name__=='__main__':
    unittest.main()
