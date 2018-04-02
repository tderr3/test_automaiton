
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime, os, sys, unittest, xmlrunner
from ctypes.test import TestRunner


def configure():
    global lxcaIp, lxcaUn, lxcaPw
    lxcaIp = '10.243.1.100'
    lxcaUn = 'USERID'
    lxcaPw = 'CME44len'


class Bundle_download_link_test(unittest.TestCase):
    
    def setUp(self):
        self.dr = webdriver.Firefox()
        self.dr.implicitly_wait(10)
        self.dr.maximize_window()
        self.dr.get('https://'+'10.243.10.71')
        self.dr.find_element_by_xpath('//input[contains(@placeholder,"user")]').send_keys('USERID')
        self.dr.find_element_by_xpath('//input[contains(@placeholder,"password")]').send_keys('CME44len')
        self.dr.find_element_by_xpath('//span[contains(text(),"Log In")]').click()
        time.sleep(3)
        
    def test_001_Driver_page_download_linl(self):
        try:
            self.dr.find_element_by_id('provisioning').click()
            self.dr.find_element_by_link_text('Manage OS Images').click()
            self.dr.find_element_by_xpath('//span[2][contains(@id,"ManageOSImageDriversTab")]').click()
            self.dr.find_element_by_id('manageOSImagesdriversGrid_bundleDropDown').click()
            time.sleep(2)
            self.dr.find_element_by_xpath('//td[2][contains(@id, "manageOSImagesdriversGrid_downloadBundleMenu")]').click()
            time.sleep(10)
            main_window = self.dr.window_handles[0]
            new_window = self.dr.window_handles[1]
            self.dr.switch_to_window(new_window)
            time.sleep(1)
            self.assertTrue(self.dr.find_element_by_link_text('OS Support Center').is_displayed())
            time.sleep(1)
            self.dr.switch_to_window(main_window)
            
            
        except Exception as ex:
            self.dr.switch_to_window(main_window)
            #self.dr.switch_to_window(main_window)
            self.fail(ex)
            
    def tearDown(self):
        self.dr.close()

            
            
            
if __name__=='__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='c:\\pydata\\testReport_'+str(datetime.date.today())),failfast=False, buffer=False, catchbreak=False)
    
    