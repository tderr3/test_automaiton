from selenium import webdriver
import time, flexcatSetup, unittest, xmlrunner, datetime
from test.test_datetime import setUpClass


class test_custom_os_profile(unittest.TestCase):
    
    
    @classmethod
    def setUpClass(inst):
        inst.dr = webdriver.Firefox()
        inst.dr.implicitly_wait(15)
        inst.dr.maximize_window()
        global condata, provisioning, manageOsImages
        condata = ['10.243.1.90','USERID', 'CME44len']
        flexcatSetup.setupremoteserver(condata[0], condata[1], condata[2])
        
        #login
        inst.dr.get('https://'+condata[0])
        inst.dr.find_element_by_xpath('//input[contains(@placeholder,"user")]').send_keys(condata[1])
        inst.dr.find_element_by_xpath('//input[contains(@placeholder,"password")]').send_keys(condata[2])
        inst.dr.find_element_by_xpath('//span[contains(text(),"Log In")]').click()
        
        #to do Import sles 12.2
        provisioning = inst.dr.find_element_by_id('provisioning')
        manageOsImages=inst.dr.find_element_by_link_text('Manage OS Images')
        
        provisioning.click()
        manageOsImages.click()
        
        inst.dr.find_element_by_xpath('.//*[@id="flexcat_manageOSImage_ManageOSImage_0_importOSBtn"]').click()
        inst.dr.find_element_by_xpath('//span[2][text()="Remote Import"]').click()
        inst.dr.find_element_by_xpath('//input[@placeholder="example: /isos/VMWare/6.0u1/LNV2016.iso"]').send_keys('/images/SLES/SLES_12_2.iso')
        
        
        

    def Test_001_import_unattend(self):
        #todo
        
    def Test_002_import_custom_config(self):
        #todo
        
    def Test_003_import_import_software_payload(self):
        #todo
    
    def Test_004_import_Post_install_script(self):
        #todo
    
    def Test_005_associate_unattend_and_config(self):
        #todo
    
    def Test_005_create_custom_profile(self):
        #todo
    
    
    @classmethod
    def tearDownClass(inst):
        #todo
        
    
if __name__=='__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='\\os_deploy_test_results'+str(datetime.date.today())),failfast=False, buffer=False, catchbreak=False)