import requests, time, sys, unittest, xmlrunner, warnings, datetime


warnings.filterwarnings('ignore')

class test_os_deploy_suite(unittest.TestCase):        
    @classmethod
    def setUpClass(inst):
        global lxcaip, targetUUID, un, pw, host
        lxcaip = '10.243.1.100'
        un = 'USERID'
        pw = 'CME44len'
        targetUUID = 'ACBA630A078C11E89143DCCBD13D789D'
        host = 'https://'+lxcaip
        
        #setting global settings
        '''payload1 = {'credentials': [{'type': 'LINUX', 'password': 'CME44len', 'passwordChanged': True}, {'type': 'ESXi', 'password': 'CME44len', 'passwordChanged': True}, {'type': 'RHEL/ESXi', 'password': 'CME44len', 'passwordChanged': True}, {'type': 'WINDOWS', 'password': 'CME44len', 'passwordChanged': True}]}
        globalset = requests.put(host+'/osdeployment/globalSettings', auth =(un,pw), verify=False, json = payload1)
        if globalset.code != 200:
            print('Global settings failed! fix to continue')
            quit()'''
            
        #checking target UUID is managed
        '''uuidCheck = requests.get(host+'/nodes/'+targetUUID)
        if uuidCheck.json()['status']['name'] == 'UNMANAGED':
            print('target server is not managed')
            quit()
        elif uuidCheck.status_code == 404:
            print('Server not found possible invalid UUID was provided')
        elif uuidCheck.json()['status']['name'] == 'MANAGED':
            print('Server managed')'''

        
        #check if os images have been imported
        #todo
        
        
    def test_001_esxi(self):
        payload = [{"networkSettings":{"gateway":"10.243.0.1","ipAddress":"10.243.1.108","selectedMac":'AUTO',"subnetMask":"255.255.240.0"},"selectedImage":"esxi6.5_0.14|esxi6.5_0.14-x86_64-install-Virtualization","storageSettings":{"targetDevice":"localdisk"},"uuid":targetUUID}]
        test = requests.put(host+'/hostPlatforms',auth=(un,pw), verify=False, json=payload)
        self.assertEqual(test.json()['result'], 'success', test.json()['messages'])
        jobid = test.json()['jobId']
        jobStatus = self.jobTracker(jobid)
        self.assertEqual(jobStatus.json()[0]['status'], 'Complete', jobStatus.json()[0]['status'])
            
            
            
    def test_002_rhel(self):
        payload = [{"networkSettings":{"gateway":"10.243.0.1","ipAddress":"10.243.1.108","selectedMac":'AUTO',"subnetMask":"255.255.240.0"},"selectedImage":"rhels7.4|rhels7.4-x86_64-install-Basic","storageSettings":{"targetDevice":"localdisk"},"uuid":targetUUID}]
        test = requests.put(host+'/hostPlatforms',auth=(un,pw), verify=False, json=payload)
        self.assertEqual(test.json()['result'], 'success', test.json()['messages'])
        jobid = test.json()['jobId']
        jobStatus = self.jobTracker(jobid)
        self.assertEqual(jobStatus.json()[0]['status'], 'Complete', jobStatus.json()[0]['status'])
        time.sleep(60)        
    
    
    '''def test_003_windows(self):
        payload = [{"networkSettings":{"gateway":"10.243.0.1","ipAddress":"10.243.1.108","selectedMac":'AUTO',"subnetMask":"255.255.240.0"},"selectedImage":"win2016|win2016-x86_64-install-Datacenter","storageSettings":{"targetDevice":"localdisk"},"uuid":targetUUID}]
        test = requests.put(host+'/hostPlatforms',auth=(un,pw), verify=False, json=payload)
        self.assertEqual(test.json()['result'], 'success', test.json()['messages'])
        jobid = test.json()['jobId']
        jobStatus = self.jobTracker(jobid)
        self.assertEqual(jobStatus.json()[0]['status'], 'Complete', jobStatus.json()[0]['status'])
    
    
    def test_004_sles(self):
        payload = [{"networkSettings":{"gateway":"10.243.0.1","ipAddress":"10.243.1.108","selectedMac":'AUTO',"subnetMask":"255.255.240.0"},"selectedImage":"sles12.2|sles12.2-x86_64-install-Basic-kISO","storageSettings":{"targetDevice":"localdisk"},"uuid":targetUUID}]
        test = requests.put(host+'/hostPlatforms',auth=(un,pw), verify=False, json=payload)
        self.assertEqual(test.json()['result'], 'success', test.json()['messages'])
        jobid = test.json()['jobId']
        jobStatus = self.jobTracker(jobid)
        self.assertEqual(jobStatus.json()[0]['status'], 'Complete', jobStatus.json()[0]['status'])'''
    
    
    
    
    @classmethod
    def tearDownClass(inst):
        print('done')
        
        
    def jobTracker(self,jid):
        job_data = requests.get(host+'/tasks/'+ str(jid), verify = False , auth=(un, pw))
        job_status = job_data.json()[0]['status']
        while job_status == 'Running' or job_status == 'Pending':
            job_data = requests.get(host+'/tasks/'+ str(jid), verify = False , auth=(un, pw))
            job_status = job_data.json()[0]['status']
            time.sleep(5)
        return job_data
             

if __name__=='__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='c:\\Data\\os_deploy_test_results'+str(datetime.date.today())),failfast=False, buffer=False, catchbreak=False)    