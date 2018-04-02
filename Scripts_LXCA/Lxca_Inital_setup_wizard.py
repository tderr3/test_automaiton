from selenium import webdriver
from datetime import datetime
import time, unittest, os, HtmlTestRunner, shutil, xmlrunner
#import flexcatSetup
from selenium.webdriver.common import action_chains, keys



class Lxca_Initial_Setup_Test(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        profile = webdriver.FirefoxProfile(os.path.normpath('c:/Automation_web/ffprofile/'))
        profile.accept_untrusted_certs = True
        inst.driver = webdriver.Firefox(profile)
        inst.driver.implicitly_wait(5)
        inst.driver.maximize_window()
        #inst.driver.get('https://'+lxcaip)
        inst.driver.get('https://10.243.1.100')
        

    def test_001_Accepting_License_Agreement(self):
        self.driver.find_element_by_xpath('//b[contains(text(),"Read and Accept Lenovo® XClarity Administrator License Agreement")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Accept")]').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath('//div[1][contains(@class, "floatLeft setupLicense completed")]'),msg='Accepting License Agreement did not complete')
        time.sleep(2)

    def test_002_Create_User_Accounts(self):
        self.driver.find_element_by_xpath('//b[contains(text(),"Create User Account")]').click()
        time.sleep(1)
        user1 = self.driver.find_element_by_xpath('//input[contains(@placeholder,"Username")]')
        pass1 = self.driver.find_element_by_xpath('//input[contains(@placeholder,"New password")]')
        pass2 = self.driver.find_element_by_xpath('//input[contains(@id , "confirmPassword")]')
        
        user1.send_keys('USERID')
        pass1.send_keys('CME44len')
        pass2.send_keys('CME44len')
        time.sleep(.5)
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Create")][contains(@id,"submitButtonForm")]').click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element_by_xpath('//td[1][contains(text(),"USERID")]'), msg='USERID was not created')

        self.driver.find_element_by_xpath('//span[contains(@title,"Create New User")]').click()
        time.sleep(2)
        user1 = self.driver.find_element_by_xpath('//input[contains(@placeholder,"Username")]')
        pass1 = self.driver.find_element_by_xpath('//input[contains(@placeholder,"New password")]')
        pass2 = self.driver.find_element_by_xpath('//input[contains(@id , "confirmPassword")]')
        user1.send_keys('USER01')
        pass1.send_keys('CME44len')
        pass2.send_keys('CME44len')
        time.sleep(.5)
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Create")][contains(@id,"submitButtonForm")]').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath('//td[1][contains(text(),"USER01")]'), msg='USER01 was not created')
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Return to Initial Setup")]').click()
        time.sleep(1)
        
        self.assertTrue(self.driver.find_element_by_xpath('//div[1][contains(@class,"floatLeft setupUserAccount completed")]'), msg='Create User Accounts did not complete')

    def test_003_Configure_network_settings(self):
        time.sleep(2)
        self.driver.find_element_by_xpath('//div[3]/b[contains(text(),"Configure Network Access")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//span/span[contains(text(),"discover and manage hardware only.")]').click()
        time.sleep(.5)
        self.driver.find_element_by_xpath('//table/tbody/tr[1]/td[2][contains(text(),"images")]').click()
        time.sleep(.5)
        self.driver.find_element_by_xpath('//span/span/span[3][contains(text(),"Save IP Settings")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//span[2]/span[1]/span/span/span[3][contains(text(),"Save")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//span[3][contains(text(), "Cancel")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//span/span[3][contains(text(),"Return to Initial Setup")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Close")]').click()
        time.sleep(2)
        
        self.assertTrue(self.driver.find_element_by_xpath('//div[1][contains(@class,"floatLeft setupNetworkAccess completed")]'),msg='Network configuration did not complete')
        
    def test_004_Configure_NTP_settings(self):
        self.driver.find_element_by_xpath('//div[3]/b[contains(text(),"Configure Date and Time Preferences")]').click()
        time.sleep(4)
        self.driver.find_element_by_xpath('//div/span[1]/span/span/span[3][contains(text(),"Save")]').click()
        time.sleep(3)
        self.assertTrue(self.driver.find_element_by_xpath('//div[1][contains(@class,"setupDateAndTime completed")]'),msg='NTP configuration did not complete')
           

    def test_005_Usage_Data_settings(self):
        self.driver.find_element_by_xpath('//div[1][contains(@class, "setupServiceAndSupport")]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//input[contains(@name,"feedBackRadioOptions")][contains(@value,"no")]').click()
        time.sleep(2)
        
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Apply")]').click()
        time.sleep(3)
        self.assertTrue(self.exCheck('//img[contains(@src,"/ui/lxca/customUI/logs/initialSetup/images/fb-data.png")]'))


    def test_006_Callhome_settengs(self):
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Skip Step")]').click()
        time.sleep(2)
        self.assertTrue(self.exCheck('//img[contains(@src,"/ui/lxca/customUI/logs/initialSetup/images/call-home.png")]'))


    def test_007_Lenovo_Upload_Facility(self):
        self.driver.find_element_by_xpath('//span/span[3][contains(text(),"Skip Step")]').click()
        time.sleep(2)
        self.assertTrue(self.exCheck('//img[contains(@src,"/ui/lxca/customUI/logs/initialSetup/images/Lenovo-Upload.png")]'))
    
    def test_008_warranty(self):
        time.sleep(2)
        self.driver.find_element_by_xpath('//span[3][contains(text(),"Skip Step")]').click()
        time.sleep(2)
        self.assertTrue(self.exCheck('//img[contains(@src,"/ui/lxca/customUI/logs/initialSetup/images/waranty.png")]'))
        self.driver.find_element_by_xpath('//div[contains(text(),"Return to Initial Setup")]').click()


    def test_009_setup_Service_and_Support(self):
        self.assertTrue(self.driver.find_element_by_xpath('//div[1][contains(@class,"floatLeft setupServiceAndSupport completed")]'),msg='setup Service and Support did not complete')

    
    def test_010_Finish(self):
        self.driver.find_element_by_xpath('//div[2]/div[3]/b[contains(text(),"Start Managing Systems")]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//span/span/span/span[3][contains(text(),"No")]').click()
        time.sleep(4)

    '''def test_011_test_fail_example(self):
        self.assertEquals('Expected Results', 'Actual Results', msg= 'The Actual Results did not match the Expected Results')

    def test_012_test_error_example(self):
        self.driver.find_element_by_id('some_fake_element')'''
        



    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()

    def exCheck(self, path):
        try:
            self.driver.find_element_by_xpath(path)
        except Exception as ex:
            
            if 'Unable to locate element' in (str(ex)):
                return True
            else:
                print(str(ex))
                return False
                

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False)       


        
