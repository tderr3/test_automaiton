from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidElementStateException
import unittest, os, csv, sys, datetime, win32gui, win32api, win32con, xmlrunner,time
import requests, json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


#import HTMLTestRunner

def Is_element_exist(self, element_name, element_des):
    element_des = element_des.replace(" ", "_")
    j = 1
    for i in range(5):
        if i == j:
            print "     Try " + str(i) + " times, also failed"
            
            scname = "Screenshot_" + str(element_des) + "_.jpg"
            self.driver.save_screenshot(scname)
            return False
        else:
            try:
                self.driver.find_element_by_xpath(element_name)
                print "     Find element: ", element_des
                sleep(2)
                self.driver.implicitly_wait(30)
                return True
            except NoSuchElementException:
                print "     Not find element with loop : " + str(i+1) + " -- " + str(element_des) + ". Wait " + str((i+1)*(i+1))  + "s and try again"
                sys.stdout.flush()
                sleep((i+1)*(i+1)) 
    
##########

def wait_time(max_time):
    for n in range(0,max_time,1):
        sleep(1)
        sys.stdout.flush()
        sys.stdout.write("\r"+str(n)+" / " + str(max_time) + " \r" ) 
###########################

def get_lxca_version_before_wzd(ipv6_url):
    global lxca_release
    lxca_verion_filename = "xClarity_version.txt"
    if os.path.exists(lxca_verion_filename):          os.remove(lxca_verion_filename)   
    data = ""
    lxca_url = ipv6_url + "/xHMC/Settings"

    for i in range(2):
        try:
            print "0000000000-: ", i
            LXCA_info = requests.get(lxca_url, auth=('AUTOWZD', 'Passw0rd'), verify =False)
            print LXCA_info
            data = json.loads(LXCA_info.content)
            break
        except Exception, e:
            print "Get lxca version failed " + str(i+1) + "time, lxca url: ", lxca_url
            print "Detail information is: ", e
            print "\nWait 300s try again"
            sleep(300)
    if data:
        
        lxca_release = data['version']
        lxca_build = data['build']
        lxca_version = lxca_release + "-" + lxca_build
        print "Success to get LXCA: " + ipv6_url + " version is: " + lxca_version
        
        lxca_verion_file = open(lxca_verion_filename, 'w')
        lxca_verion_file.write(lxca_version)
        lxca_verion_file.close()
    else:
        print "Failed to get LXCA: " + ipv6_url + " version and set to empty"
        lxca_release = ""
        
    
#####################

def get_lxca_info_from_config():
    global ipv6_url, ipv4_static_ip, ipv6_static_ip, ip_mask, ipv4_gateway,ipv6_gateway, lxca_user0, lxca_user1, lxca_pwd, ipv6_add, lxca_name, vmware_host, lxca_name_IPv6
    lxca_config = open(config_txt, 'r')
    for lxca in lxca_config:
        lxca_key = lxca.split('__')[0]
        if lxca_key=="VMwareHost":  vmware_host = lxca.split('__')[1].strip('\n')
        if lxca_key=="lxca_name":  lxca_name = lxca.split('__')[1].strip('\n')
        if lxca_key=="lxca_name_IPv6":  lxca_name_IPv6 = lxca.split('__')[1].strip('\n')
        if lxca_key=="IPv4_add":  ipv4_static_ip = lxca.split('__')[1].strip('\n')
        if lxca_key=="IPv6_add":  ipv6_static_ip = lxca.split('__')[1].strip('\n')
        if lxca_key=="IP_mask":  ip_mask = lxca.split('__')[1].strip('\n')
        if lxca_key=="IPv4_gateway":  ipv4_gateway = lxca.split('__')[1].strip('\n')
        if lxca_key=="IPv6_gateway":  ipv6_gateway = lxca.split('__')[1].strip('\n')
        if lxca_key=="LXCA_user0":  lxca_user0 = lxca.split('__')[1].strip('\n')
        if lxca_key=="LXCA_user1":  lxca_user1 = lxca.split('__')[1].strip('\n')
        if lxca_key=="LXCA_pwd":  lxca_pwd = lxca.split('__')[1].strip('\n')
    if "ipv6" in opt_job.lower():
        lxca_name = lxca_name_IPv6
    lxca_config.close()
    
####################

def get_vmware_info_by_powershell():
    
    if os.path.exists(csv_file): os.system("del /f " + csv_file)
    #os.system("powershell Set-ExecutionPolicy Unrestricted")
    #os.system("powershell Set-ExecutionPolicyRemoteSigned")
    #os.system("powershell Set-ExecutionPolicyAllSigned")
    #os.system("powershell -noe -c .\\test.ps1 " + config_txt)
    os.system("powershell -noe -c .\\test.ps1 -vm_host_config " + config_txt + " -type get_vm_host")
####################

def get_lxca_info_from_csv():
    global ipv6_add
    if os.path.exists(csv_file):  
        reader = csv.reader(open(csv_file))
        for aa in reader:
            if lxca_name in aa:
                if aa[5] == "PoweredOn":
                    if aa[6] !="":
                        """
                        a1 = aa[6].split(',')[0]
                        a2 = aa[6].split(',')[1]
                        if len(a1)<=15 and len(a2)>15: ipv6_add =  a2
                        if len(a1)>15 and len(a2)<15: ipv6_add = a1
                        if len(a1)>15 and len(a2)>15: ipv6_add = a1
                        """
                        #ipv6_add = aa[6].split(',')[1] or aa[6].split(',')[2]
                        #ipv6_add = ((":" in aa[6].split(' ')[1]) or (":" in aa[6].split(' ')[2]) )
                        for i in range(aa[6].count(" ")+1):
                            if ":" in aa[6].split(" ")[i]:
                                ipv6_add = aa[6].split(" ")[i]
                                break
                        break
                    else:
                        '''
                        print "Cannot get target LXCA IP address, wait 60s and try again..."
                        sleep(60)
                        if os.path.exists(csv_file): os.system("del /f " + csv_file)
                        os.system("powershell -noe -c .\\test.ps1 " + config_txt )
                        get_lxca_info_from_csv()
                        
                        print "Can not get LXCA " + str(lxca_name) + "'s IP address. Please manual check it"
                        sys.stdout.flush()
                        sys.exit(-1)
                        '''
                        print "Get LXCA " + str(lxca_name) + " Powered-On, but cannot get its IP address. Auto exit"
                        sys.exit(-1)
                        
                        '''
                        print "Get LXCA " + str(lxca_name) + " Powered-On, but cannot get its IP address. Restart it by PowerCLI"
                        os.system("powershell -noe -c .\\test.ps1 -vm_host_config " + config_txt + " -type restart_vm_client -vm_client " + str(lxca_name))
                        print "Restart " + lxca_name + " completed, wait 420s to run Wizard"
                        sleep(420)
                        get_vmware_info_by_powershell()
                        get_lxca_info_from_csv()
                        '''
       
                else:
                    print "Warning!!! Target LXCA '" + lxca_name + "' was PowerOff status, PowerOn it by PowerCLI" 
                    os.system("powershell -noe -c .\\test.ps1 -vm_host_config " + config_txt + " -type poweron_vm_client -vm_client " + str(lxca_name))
                    print "PoweredOn " + lxca_name + " completed, wait 420s to run Wizard"
                    sleep(420)
                    get_vmware_info_by_powershell()
                    get_lxca_info_from_csv()
    else:
        print "Warning!!! Do not find 'vmlist.csv' file, please re-execute it..."
        sys.stdout.flush()
        exit()
######################

def close_windows_window():
    classname = "MozillaDialogClass"
    titlename = "Add Security Exception"
    hwnd = win32gui.FindWindow(classname,titlename)
    (left,top,right,bottom) = win32gui.GetWindowRect(hwnd)
    win32gui.SetForegroundWindow(hwnd)
    print left, top, right, bottom
    win32api.SetCursorPos([int(right)-120,int(bottom)-20])

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
##########################

def lxca_service_restart(self):
    ### Click 'Save' button on 
    #self.driver.find_element_by_xpath("//span[contains(.,'Save')]").click()
    self.driver.find_element_by_xpath("//span[contains(.,'Save IP Settings')]").click()
    sleep(2)
    self.driver.implicitly_wait(30)
                        
    ### Click 'Save' button after pop-up 'Save' dialog
    self.driver.find_element_by_xpath("//*[@class='messageAction']/span[1]/span[1]/span[1]").click()  
    sleep(2)
    self.driver.implicitly_wait(30)
    
    print "     Try to get 'Restart' button and click it"
    attempts = 0
    max_loop = 40
    while attempts < max_loop:
        try:
            self.driver.find_element_by_xpath("//span[@class='messageAction']//span[text()='Restart']").click()
            sleep(2)
            self.driver.implicitly_wait(30)
            print "     Success to get and click Restart button"
            break
        except NoSuchElementException:
            attempts +=1
            #print "Cannot get Restart button. Sleep 10s and try again, loop: " + str(attempts) + "/" + str(max_loop)
            sleep(10)
            
            if attempts == max_loop:
                print "Try " + str(attempts) + " times(10s pre one time) and also can not get 'Restart' button"
                
                scname = "Screenshot_Config_Network_Access.jpg"
                self.driver.save_screenshot(scname)
                print "Screen captured: "+scname
                self.assertEqual("Pass","Fail")
                self.driver.close()
    """        
    ### Click 'Restart' button
    self.driver.find_element_by_xpath("//span[@class='messageAction']//span[text()='Restart']").click()         
    sleep(2)
    self.driver.implicitly_wait(30)
    """
    
##############################

def login_lxca(self):
    sleep(3)
    self.driver.find_element_by_id("idx_form_TextBox_0").send_keys(lxca_user_wzd)
    self.driver.find_element_by_id("augusta-login-framePassword").send_keys(lxca_pwd)
    self.driver.find_element_by_id("dijit_form_Button_0").click()
    self.driver.implicitly_wait(30)
    sleep(3)
####################################3


class LXCA_Wizard(unittest.TestCase):
    def setUp(self):
        #self.profile = webdriver.FirefoxProfile(r"C:\\FFprofile")
        #self.driver = webdriver.Firefox(self.profile)
        #self.driver = webdriver.Firefox()
        
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        #self.chrome = "C:\Python27\selenium\webdriver\chromedriver.exe"
        self.chrome = os.path.dirname(os.path.realpath(__file__))+"\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = self.chrome
        self.driver = webdriver.Chrome(self.chrome,chrome_options=options)
        
        driver = self.driver
        driver.maximize_window()
        driver.implicitly_wait(30)
        driver.get(ipv6_url)
        driver.implicitly_wait(60)
        
    ### License Agreement
    ################################
    def Add_Exception(self):
        Register = False
        try:
            self.driver.find_element_by_xpath("//button[@id='advancedButton']")
            Register = True
        except:
            Register = False
        if Register:
            self.driver.find_element_by_xpath("//button[@id='advancedButton']").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_xpath("//button[@id='exceptionDialogButton']").click()
            self.driver.implicitly_wait(30)
            close_windows_window()
            self.driver.implicitly_wait(30)
    #######################
        
    def License_Agreement(self):
        ##########################
        print "1/8 - Start License Agreement..."
        sys.stdout.flush()
        try:
            try:
                print "     Try click License agreement or skip it"
                sys.stdout.flush()
                self.driver.find_element_by_xpath(".//*[@id='dijit__TemplatedMixin_1']/div[2]/div[3]/b").click()  ## Click to enter License page
                self.driver.implicitly_wait(30)
                
                try:
                    print "     Click Accept complete License Agreement"
                    self.driver.find_element_by_xpath("//span[contains(.,'Accept')]").click()
                    sleep(3)
                    print "      Finished License agreement"
                    sys.stdout.flush()
                except InvalidElementStateException :
                    try:
                        print "     Already completed License Agreement, click 'Return to Initial Setup' skip"
                        self.driver.find_element_by_xpath("//span[contains(.,'Return to Initial Setup')]").click()
                        sleep(3)
                        print "      Return to Initial Setup direct"
                        sys.stdout.flush()
                    except NoSuchElementException:
                        print "     Config License Agreement failed"
                        sys.stdout.flush()
            except NoSuchElementException:
                print "     Have been completed License Agreement, goto UserAccount page direct"
                sys.stdout.flush()
                login_lxca(self)
            
            
            
            
            
            """
            #### Create account - AUTOWZD
            print "\n2/8 - Start create account: AUTOWZD "
            sys.stdout.flush()
            
            try:
                print "     Checking whether existing Account-Dialog"
                sys.stdout.flush()
                
                element_des = "Checking Account-Dialog auto pop up or not"
                element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_cancelButtonForm_label']"
                if Is_element_exist(self, element_name , element_des):
                    print "     Get 'Create Supervisor User dialog', and close it"
                    self.driver.find_element_by_xpath(element_name).click()
                    self.driver.implicitly_wait(30)
                    sleep(3)
                    
                    element_des = "Checking Account: " + str(lxca_user_wzd) + " existing or not"
                    element_name = "//td[contains(.,'"+lxca_user_wzd+"')]"
                    if Is_element_exist(self, element_name , element_des):
                        print "     Get Account: " +str(lxca_user_wzd) + " existing , and delete it"
                        
                        for i in range(3):
                            self.driver.find_element_by_xpath(".//*[@id='usersManagementActualGrid']/div[3]/div[4]/div[" + str(i+1) +"]/table/tbody/tr/td/span").click()
                            self.driver.implicitly_wait(30)
                            sleep(3)
                            
                            element_des = "Click UserAccount delete button"
                            element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_deleteBtn']/span[1]"
                            if Is_element_exist(self, element_name , element_des):
                                self.driver.find_element_by_xpath(element_name).click()
                                self.driver.implicitly_wait(30)
                                sleep(3)
                            
                            element_des = "Checking and close 'Confirm delete UserAccount' dialog"
                            element_name = ".//*[@class='messageDialogFooter']/span[2]/span[1]/span/span/span[3]"
                            
                            #self.driver.find_element_by_xpath(".//*[@id='usersManagementActualGrid']/div[3]/div[4]/div[" + str(i+1) +"]/table/tbody/tr/td/span")
                            
                            if Is_element_exist(self, element_name , element_des):
                                self.driver.find_element_by_xpath(element_name).click()
                                self.driver.implicitly_wait(30)
                                sleep(3)
            except Exception, e:
                print "     Have no Account-Dialog auto popup"
                sys.stdout.flush()
            
            
            element_des = "Click 'Create New User' button"
            #element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_addBtn']/span[1]"
            element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_listViewGrid']/div/div[2]/div[1]/table/tbody/tr/td[1]/div/span[1]/span/span/span[1]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(3)                
                
                ## Input Account name
                self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0usernameNode").send_keys(lxca_user_wzd)  
                self.driver.implicitly_wait(30)
                ## Input Account pwd
                self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0newPassword").send_keys(lxca_pwd)
                self.driver.implicitly_wait(30)  
                ## confirm Account pwd
                self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0confirmPassword").send_keys(lxca_pwd) 
                self.driver.implicitly_wait(30)
                ## Click "Save" button to save and close create account dialog
                self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0_submitButtonForm_label").click()  
                self.driver.implicitly_wait(30)
                sleep(3)
                
                print "      Finished AUTOWZD creation"
                sys.stdout.flush()
            """
        except Exception, e:
            print e
            scname = "Screenshot_License_2_Create_USERID.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
            #self.driver.close()
    ###########################
        
    #### Create multi accounts & password
    ##########################################
    def Create_Multi_LXCA_Accounts(self):
        try:
            
            sleep(4)
            try:
                print "      Try check whether need Login to create multi accounts"
                sys.stdout.flush()
                login_lxca(self)
            except:
                print "      No need Login to create multi accounts"
                sys.stdout.flush()
            
            #### Create Multi accounts
            print "   - Start multi accounts creation"
            sys.stdout.flush()
            sleep(3)
            self.driver.find_element_by_xpath(".//*[@id='dijit__TemplatedMixin_2']/div[2]/div[3]/b").click()
            self.driver.implicitly_wait(30)
            sleep(3)
            
            element_des = "Checking Account-Dialog auto pop up or not"
            element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_cancelButtonForm_label']"
            if Is_element_exist(self, element_name , element_des):
                print "     Get 'Create Supervisor User dialog', and close it"
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(3)
            
        
            multi_accounts_arr = [lxca_user_wzd, lxca_user0, lxca_user1,"AUTOAPI","AUTOPY","AUTOPS", "AUTOUI"]
            need_create_account = []
            print "     Total accounts are: ", multi_accounts_arr
            
            for user in multi_accounts_arr:
                try:
                    self.driver.find_element_by_xpath("//td[contains(.,'"+user+"')]")
                    print "     Existing account: " + str(user) + ", no need create"
                except NoSuchElementException:
                    print "     Have no account : " + str(user) + ", need create it"
                    need_create_account.append(user)
            
            if len(need_create_account) == 0:
                print "     All accounts existed, no need create"
            else:
                print "     Need create account are: ", need_create_account
                for user in need_create_account:
                    try:
                        print "      Do not pop up 'Create User' dialog, click 'New' to create " + user
                        self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0_actionBtn_label").click()
                        self.driver.implicitly_wait(30)
                        #self.driver.find_element_by_xpath(".//*[@id='dijit_MenuItem_8_text']").click()
                        #self.driver.find_element_by_xpath("//span[contains(.,'Create New User')]").click()
                        create_new_user_btn = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_listViewGrid']/div/div[2]/div[1]/table/tbody/tr/td[1]/div/span[1]/span/span/span[1]"
                        self.driver.find_element_by_xpath(create_new_user_btn).click()
                        self.driver.implicitly_wait(30)
                        sleep(1)
                    except NoSuchElementException:
                        print "      Pop up 'Create User' dialog"
                    sleep(1)
                    ##USERID1
                    self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0usernameNode").send_keys(user)
                    self.driver.implicitly_wait(30)
                    sleep(1)
                    self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0newPassword").send_keys(lxca_pwd)
                    self.driver.implicitly_wait(30)
                    sleep(1)
                    self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0confirmPassword").send_keys(lxca_pwd)
                    self.driver.implicitly_wait(30)
                    sleep(1)
                    self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0_submitButtonForm_label").click()
                    self.driver.implicitly_wait(30)
                    sleep(5)

            ## Click "Return to Initial Setup" button return to main page
            self.driver.find_element_by_xpath("//span[contains(.,'Return to Initial Setup')]").click()
            print "      Finished multi account creation"
            sys.stdout.flush()
        except Exception, e:
            print e
            scname = "Screenshot_Create_USERID1.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
            #self.driver.close()
    #########################
    
    ###########Config  Network
    ###############################################
    def Config_Network_Access(self):
        try:
            login_lxca(self)
            
            print "\n3/8 - Start Network Config..."
            sleep(5)
            sys.stdout.flush()
            self.driver.find_element_by_xpath(".//*[@id='dijit__TemplatedMixin_3']/div[2]/div[3]/b").click()
            self.driver.implicitly_wait(30)
            sleep(3)
            
            element_des = "Checking Network Dialog popup or not when enter Network page"
            element_name = ".//div[starts-with(@widgetid,'idx_widget_ModalDialog_')]"
            if Is_element_exist(self, element_name , element_des):
                dialogs = self.driver.find_element_by_xpath(element_name)
                for dialog in range(len(dialogs)):
                    widgetid = 'idx_widget_ModalDialog_'+str(len(dialogs)-1-dialog);
                    self.driver.find_element_by_xpath("//div[@widgetid='"+widgetid+"']/div[@class='messageDialogFooter']/span[@class='messageAction']/span/span").click()
                    self.driver.implicitly_wait(30)
                    print "      Try check whether networkAccess dialog(first time) pop up, content include 'If your Network Access...IPv4 to Static IPv6 mode'"
                    sys.stdout.flush()
                    sleep(4)
            else:
                print "      NetworkAccess dialog(first time) do not pop up..."
                sys.stdout.flush()
            
            element_des = "Click ETH0 drop-down button"
            element_name = ".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_networkSelect2NicsID']/tbody/tr/td[2]/div[1]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(2)
                
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_networkSelect2NicsID_menu']/tbody/tr[1]").click()
                self.driver.implicitly_wait(30)
                sleep(2)
            else:
                print "     Cannot get select ETH0 element, select 'discover and manage hardware ... deploy os images' direct "
                
                sys.stdout.flush()
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_networkSelectID']/tbody/tr/td[2]/div[1]").click()
                self.driver.implicitly_wait(30)
                sleep(2)
                
                self.driver.find_element_by_xpath("//td[contains(.,'discover and manage hardware and manage and deploy operating system images')]").click()
                self.driver.implicitly_wait(30)
                sleep(2)

            #####   Select static IP mode            
            if "ipv6" in opt_job.lower():
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv6SelectID']/tbody/tr/td[2]/div[1]").click()
                self.driver.implicitly_wait(30)

                self.driver.find_element_by_xpath("//td[contains(.,'Use statically assigned IP address')][@colspan='2']").click()
                self.driver.implicitly_wait(30)
                

                ####### Set static Ipv6
                IP_add = self.driver.find_element_by_id("lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv6AddressID")
                IP_add.clear()
                self.driver.implicitly_wait(30)
                IP_add.send_keys(ipv6_static_ip)
                
                ######  Set Prefix
                IP_mask = self.driver.find_element_by_id("lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv6NetmaskID")
                IP_mask.clear()
                self.driver.implicitly_wait(30)
                IP_mask.send_keys("64")
                
                ######  Set Gateway
                IP_gateway = self.driver.find_element_by_id("lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_defaultGwTxtBoxIpv6")
                IP_gateway.clear()
                self.driver.implicitly_wait(30)
                IP_gateway.send_keys(ipv6_gateway)
                self.driver.implicitly_wait(30)

                ########## Disable IPv4 
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv4SelectID']/tbody/tr/td[2]/div[1]").click()
                self.driver.implicitly_wait(30)
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv4SelectID_menu']/tbody/tr[3]/td[2]").click()
                self.driver.implicitly_wait(30)
                sleep(5)
                
                element_des = "Check NetworkAccess dialog(second time) exist or not"
                element_name = "//*[@class='messageAction']/span[1]/span[1]"
                if Is_element_exist(self, element_name , element_des):
                    print "      Try check whether networkAccess dialog(second time) pop up, content include 'If your Network Access...IPv4 to Static IPv6 mode'"
                    sys.stdout.flush()
                    self.driver.find_element_by_xpath(element_name).click()
                else:
                    print "      NetworkAccess dialog(second time) do not pop up..."
                    self.driver.implicitly_wait(30)
                
                sleep(5)
                    
               
            else:
                #####   Select static IP mode
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv4SelectID']/tbody/tr/td[2]/div[1]").click()
                #self.driver.find_element_by_xpath(".//*[@class='dijitReset dijitRight dijitButtonNode dijitArrowButton dijitDownArrowButton']").click()
                sleep(3)
                self.driver.implicitly_wait(30)
                self.driver.find_element_by_xpath("//td[contains(.,'Use statically assigned IP address')][@colspan='2']").click()
                self.driver.implicitly_wait(30)
                
                ####### Set static Ipv4
                IP_add = self.driver.find_element_by_id("lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv4AddressID")
                IP_add.clear()
                self.driver.implicitly_wait(30)
                IP_add.send_keys(ipv4_static_ip)
                
                ######  Set Mask
                IP_mask = self.driver.find_element_by_id("lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_eth0Ipv4NetmaskID")
                IP_mask.clear()
                self.driver.implicitly_wait(30)
                IP_mask.send_keys(ip_mask)
                
                ######  Set Gateway
                IP_gateway = self.driver.find_element_by_id("lxca_customUI_networkAccess_editNetworkAccess_editNetworkAccess_0_ipSettings_defaultGwTxtBoxIpv4")
                IP_gateway.clear()
                self.driver.implicitly_wait(30)
                IP_gateway.send_keys(ipv4_gateway)
                self.driver.implicitly_wait(30)
            ###############################
            lxca_service_restart(self)
            print "      Wait 200s to check timeout dialog(The connection to the... could not be established) pop up or not"
            sys.stdout.flush()
            sleep(200)
            
            
            try:                    
                if self.driver.find_element_by_id("timeoutDialog_desc"):
                    print "      Pass, timeout dialog(The connection to the ... could not be established) pop up"
                    sys.stdout.flush()
            except NoSuchElementException:
                print "      Warning, timeout dialog(The connection to the ... could not be established) do not pop up"
                sys.stdout.flush()
                self.driver.find_element_by_xpath(".//*[@id='dijit_form_Button_21_label']']").click()
                lxca_service_restart(self)
            
            max_time =120
            print "      Please wait " + str(max_time) + "s to save Config...."
            sys.stdout.flush()
            sleep(max_time)
            #wait_time(max_time)
            ping_result = 1
            retry = 0
            while ping_result and retry < 7:
                if "ipv6" in opt_job.lower():
                    ping_result = os.system('ping [' + ipv6_static_ip + '] -n 2')
                else:
                    ping_result = os.system('ping ' + ipv4_static_ip + ' -n 2')
                sleep(20)
                retry +=1
                print "retry is "+ str(retry)
            sys.stdout.flush()
            sleep(90)
            if "ipv6" in opt_job.lower():
                self.driver.get(ipv6_static_url)
            else:
                self.driver.get(ipv4_static_url)
            self.driver.implicitly_wait(30)
            print "      Finished Network Config..."
            sys.stdout.flush()
        except Exception, e:
            print e
            scname = "Screenshot_Config_Network_Access.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
            #self.driver.close()
    ##########################
    
    ###########Config  Data and time
    ###############################################
    def Config_Date_and_Time(self):    
        #########   Config Date and Time
        #####################
        try:
            if "ipv6" in opt_job.lower():
                self.driver.get(ipv6_static_url)
            
            login_lxca(self)
            
            print "\n4/8 - Start Date&Time Config..."
            
            self.driver.find_element_by_xpath("//div[@class='setupStepTitle']//b[text()='Configure Date and Time Preferences']").click() #  click second 'save' button
            sleep(3)
            
            ####    Select China Area
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_dateTime_editDateTime_editDateTime_0_timezoneDisplayID']/tbody/tr/td[1]/span/span").click()
            self.driver.implicitly_wait(30)
            sleep(3)
            self.driver.find_element_by_xpath("//td[contains(.,'UTC +08:00, China Standard Time')]").click()
            self.driver.implicitly_wait(30)
            sleep(2)
            #self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_dateTime_editDateTime_editDateTime_0_ntpServerHostNameTxtBox']").clear()
            #self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_dateTime_editDateTime_editDateTime_0_ntpServerHostNameTxtBox']").send_keys(ntp_server)
            
            ####    Click 'Save' button
            #self.driver.find_element_by_xpath("//*[@id='dijit_layout_ContentPane_0']/span[1]/span[1]/span[1]").click()
            self.driver.find_element_by_xpath("//span[contains(.,'Save')]").click()
            self.driver.implicitly_wait(30)
            sleep(5)
            print "      Finished Date&Time Config..."
            sys.stdout.flush()
            sleep(10)
            
            
        except Exception, e:
            print e
            scname = "Screenshot_Config_Date_and_Time.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
            #self.driver.close()
    ###########################
    
    ###########Config  Service and Support Settings
    ###############################################
    def Config_Service_and_Support_Settings(self):    
        #########   Config Service_and_Support_Settings
        #####################
        try:
            if "ipv6" in opt_job.lower():
                self.driver.get(ipv6_static_url)
            
            print "\n5/8 - Start Configure Service And Support Setting..."
            login_lxca(self)
            
            
            ####    Switch to 'Configure Service And Support Settings' page
            element_des = "Check 'Configure Service And Support Settings' exist"
            element_name = "//div[@class='setupStepTitle']//b[text()='Configure Service And Support Settings']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            else:
                print "Have no 'Configure Service And Support Settings' item and skip it"
                return True

            ################################################
            ##############      Useage data         ##################
            ################################################
            element_des = "'Usage Data' link"
            element_name = ".//*[@id='lxca_core_widgets_detailsSelector_TextAbbr_0']/span"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            
            
            element_des = "'Usage Data' -- 'Sure, I'll ...' button"
            element_name = ".//*[@id='dijit_form_RadioButton_0']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            
            
            element_des = "'Usage Data' -- 'No thanks' button"
            element_name = ".//*[@id='dijit_form_RadioButton_1']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            
            element_des = "'Usage Data' -- 'Apply' buton"
            element_name = "//span[contains(.,'Apply')]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            
            ################################################
            #######                   Call Home Configuration                  #######
            ################################################
            element_des = "'Call Home Configuration' -- 'Contact Name"
            element_name = ".//*[@id='contactName']"
            text_content = "Lenovoer"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Call Home Configuration' -- 'Company Name"
            element_name = ".//*[@id='companyName']"
            text_content = "Lenovo"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Call Home Configuration' -- 'Country"
            element_name = ".//*[@id='countryAbv']"
            text_content = "CHINA"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
                self.driver.find_element_by_xpath(".//*[@id='countryAbv_popup0']/span").click()
            
            
            element_des = "'Call Home Configuration' -- 'Email"
            element_name = ".//*[@id='email']"
            text_content = "x_sw_admin@lenovo.com"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Call Home Configuration' -- 'Phone Number"
            element_name = ".//*[@id='phoneNumber']"
            text_content = "13600000000"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            element_des = "'Call Home Configuration' -- 'Street Address"
            element_name = ".//*[@id='address']"
            text_content = "template address"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Call Home Configuration' -- 'City"
            element_name = ".//*[@id='city']"
            text_content = "Shanghai"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Call Home Configuration' -- 'State or Province'"
            element_name = ".//*[@id='stateProvince']"
            text_content = "SH"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Call Home Configuration' -- 'Zip Code'"
            element_name = ".//*[@id='zipCode']"
            text_content = "123456789"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            
            element_des = "'Call Home Configuration' -- 'Apply only'"
            element_name = ".//*[@id='saveCallHomeDataOnlyIS_label']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            
            ################################################
            #######                   Lenovo Upload Facility                   #######
            ################################################
            element_des = "'Lenovo Upload Facility' -- 'Prefix'"
            element_name = ".//*[@id='idx_form_TextBox_0']"
            text_content = "Lenovo"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Lenovo Upload Facility' -- 'Email'"
            element_name = ".//*[@id='idx_form_TextBox_1']"
            text_content = "x_sw_admin@lenovo.com"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys(text_content)
            
            
            element_des = "'Lenovo Upload Facility' -- 'Apply Only'"
            element_name = ".//*[@id='saveLUFDataOnlyIS_label']"
            #element_name = "//span[contains(.,'Apply only')]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
            
            
            ################################################
            #######                          Warranty                             #######
            ################################################
            ### Click 'Warranty' -- 'Apply' button
            element_des = "'Warranty' -- 'Apply' buton"
            element_name = "//span[contains(.,'Apply')]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                sleep(5)
            else:
                element_des = "'Warranty' -- 'Skip Step' buton"
                element_name = "//span[contains(.,'Skip')]"
                print "     Find and click 'Skip Step' replace 'Apply'"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).click()
                    sleep(5)
                    
            element_des = "'Warranty' -- 'Success' dialog"
            element_name = ".//*[@class='messageAction']/span[1]/span[1]/span[1]/span[3]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                sleep(5)
            
            
            ################################################
            #######                Return to Initial Setup                       #######
            ################################################

            element_des = "'Initial Setup' -- 'Return to Initial Setup' link"
            element_name = ".//*[@id='lxca_core_widgets_detailsSelector_TextAbbr_4']/div"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                sleep(2)
                
            
            click_required = self.driver.find_element_by_xpath(".//*[@id='dijit__TemplatedMixin_5']/div[2]/div[1]")
            print "Service_And_Support_Setting_Click_required_Status: ", click_required.get_attribute('class')
            
            while "default" in click_required.get_attribute('class'): 
                self.driver.find_element_by_xpath("//div[@class='setupStepTitle']//b[text()='Configure Service And Support Settings']").click()
                sleep(3)
                element_des = "'Initial Setup' -- 'Return to Initial Setup' link"
                element_name = ".//*[@id='lxca_core_widgets_detailsSelector_TextAbbr_4']/div"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).click()
                    sleep(2)
                click_required = self.driver.find_element_by_xpath(".//*[@id='dijit__TemplatedMixin_5']/div[2]/div[1]")

            print "\n5/8 - Finished Configure Service And Support Setting"
            sys.stdout.flush()

        except Exception, e:
            print e
            scname = "Screenshot_Config_Service_And_Support_Settings.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
            #self.driver.close()
    ###########################
    
    ###########Config  Additional Security Settings
    ###############################################
    def Config_Additional_Security_Settings(self):
        try:
            if "ipv6" in opt_job.lower():
                self.driver.get(ipv6_static_url)
            
            print "\n6/8 - Start Configure Additional Security Setting..."
            sys.stdout.flush()
            login_lxca(self)
            
            self.driver.find_element_by_xpath("//div[@class='setupStepTitle']//b[text()='Configure Additional Security Settings']").click() #  click second 'save' button
            sleep(3)
            
            
            ################################################
            ############    Create LDAP account    ##################
            ################################################
            print "\n       Create LDAP Account"
            self.driver.find_element_by_xpath("//div[contains(.,'Local Users')]").click()
            account_ldap = "AUTOLDAP"
            element_des = "Checking account 'AUTOLDAP' exist or not"
            element_name = "//td[contains(.,'"+account_ldap+"')]"
            if Is_element_exist(self, element_name , element_des):
                print "     Existing account: " + str(account_ldap) + ". No need create"
                sys.stdout.flush()
            else:
                print "     Not find account: " + str(account_ldap) + ". Start to create"
                sys.stdout.flush()
                
                element_des = "Click new Account button"
                element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0_addBtn']/span[1]"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).click()
                    self.driver.implicitly_wait(30)
                    sleep(2)
                    
                    element_des = "Input Account name"
                    element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0usernameNode']"
                    if Is_element_exist(self, element_name , element_des):
                        self.driver.find_element_by_xpath(element_name).clear()
                        self.driver.find_element_by_xpath(element_name).send_keys(account_ldap)
                        self.driver.implicitly_wait(30)
                        sleep(2)
                        
                        element_des = "Input Account password"
                        element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0newPassword']"
                        if Is_element_exist(self, element_name , element_des):
                            self.driver.find_element_by_xpath(element_name).clear()
                            self.driver.find_element_by_xpath(element_name).send_keys(lxca_pwd)
                            self.driver.implicitly_wait(30)
                            sleep(2)
                            
                            element_des = "Confirm Account password"
                            element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0confirmPassword']"
                            if Is_element_exist(self, element_name , element_des):
                                self.driver.find_element_by_xpath(element_name).clear()
                                self.driver.find_element_by_xpath(element_name).send_keys(lxca_pwd)
                                self.driver.implicitly_wait(30)
                                sleep(2)
                        
                #   Click role groups drop-down btn
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0newUserRoleSelect']/tbody/tr/td[2]/div[1]").click()
                self.driver.implicitly_wait(30)
                
                #   Select roles
                element_des = "Select roles for 'AUTOLDAP'"
                for i in range(10):
                    element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0newUserRoleSelect_menu']/table/tbody/tr/td/table/tbody/tr[" + str(i+1)  +"]/td[1]/span[1]"
                    if Is_element_exist(self, element_name , element_des):
                        self.driver.find_element_by_xpath(element_name).click()
                        self.driver.implicitly_wait(10)
                    else:
                        print "Role can not selected"
                sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0newUserRoleSelect']/tbody/tr/td[2]/div[1]").click()
                self.driver.implicitly_wait(30)
                sleep(2)
                
                
                element_des = "Click Chg pwd on first access drop-down btn"
                element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0passwordChangeFirstAccessUser']/tbody/tr/td[2]/div[1]"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).click()
                    self.driver.implicitly_wait(30)
                    sleep(2)
                    element_des = "Click Chg pwd on first access drop-down btn"
                    element_name = ".//*[@id='lxca_customUI_security_usersManagement_usersManagementGrid_0passwordChangeFirstAccessUser_menu']/tbody/tr[2]/td[2]"
                    if Is_element_exist(self, element_name , element_des):
                        self.driver.find_element_by_xpath(element_name).click()
                        self.driver.implicitly_wait(30)
                        sleep(2)
                    else:
                        print "     Cannot select No"
                else:
                    print "     Cannot click 'Change password on first access' drop-down btn"
                sleep(3)
                self.driver.find_element_by_id("lxca_customUI_security_usersManagement_usersManagementGrid_0_submitButtonForm_label").click()
                self.driver.implicitly_wait(30)
                sleep(3)
            
                
            #self.driver.find_element_by_xpath("//div[contains(.,'Local Users')]").click()
            ############################################
            ########      Trusted Certificates create Cer      #########
            ###########################################
            print "\n     Create Certificate for LDAP"
            certificate_file = "certificate_for_LDAP.pem"
            certificate_file_path = current_path + "\\" + certificate_file
            print "       Certificate file path: ", certificate_file_path
            
            #self.driver.find_element_by_xpath("//td[contains(.,'UTC +08:00, China Standard Time')]").click()
            
            element_des = "Click 'Trusted Certificates' link"
            #element_name = "//div[contains(.,'Trusted Certificates')]"
            element_name = ".//*[@id='lxca_core_widgets_detailsSelector_TextAbbr_8']/div"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(2)
                
                element_des = "New a certificate"
                element_name = ".//*[@id='lxca_customUI_security_trustedCertificates_trustedCertificatesGrid_0_addButton']/span[1]"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).click()
                    self.driver.implicitly_wait(30)
                    sleep(2)
                    
                    element_des = "Click 'Install from' radio box"
                    element_name = ".//*[@id='lxca_customUI_security_trustedCertificates_trustedCertificatesGrid_0_fileMethodContainerNode']/label"
                    if Is_element_exist(self, element_name , element_des):
                        self.driver.find_element_by_xpath(element_name).click()
                        self.driver.implicitly_wait(30)
                        sleep(2)
                        
                        element_des = "Upload pem file"
                        element_name = ".//*[@id='lxca_customUI_security_trustedCertificates_trustedCertificatesGrid_0_fileMethodContainerNode']/span/input[1]"
                        if Is_element_exist(self, element_name , element_des):
                            self.driver.find_element_by_xpath(element_name).send_keys(certificate_file_path)
                            self.driver.implicitly_wait(30)
                            sleep(2)
                            
                            element_des = "Click Create btn finish certificate add"
                            element_name = ".//*[@id='lxca_customUI_security_trustedCertificates_trustedCertificatesGrid_0_runCertificateActionButton']"
                            if Is_element_exist(self, element_name , element_des):
                                self.driver.find_element_by_xpath(element_name).click()
                                self.driver.implicitly_wait(30)
                                sleep(3)
                                
                                element_des = "Click Close btn close dialog"
                                #element_name = ".//*[@class='dijitDialog idxInformationMessageDialog idxModalDialog']/div[4]/span[3]/span/span/span/span[3]"
                                #element_name = ".//*[@class='dijitDialog idxInformationMessageDialog idxModalDialog']/div[4]/span[3]/span/span/span/span[3]"
                                #self.driver.find_element_by_xpath("//span[contains(.,'Local Users')]").click()
                                #   self.driver.find_element_by_xpath("//div[@class='setupStepTitle']//b[text()='Start Managing Systems']").click() 
                                element_name = ".//*[@class='messageDialogFooter']/span[3]/span[1]/span[1]/span[1]/span[3]"
                                if Is_element_exist(self, element_name , element_des):
                                    self.driver.find_element_by_xpath(element_name).click()
                                    self.driver.implicitly_wait(30)
                                    sleep(4)
                                else:
                                    print "     Cannot find and click 'Close' btn"
                            else:
                                print "     Cannot find and click 'Create' btn"
                        else:
                            print "     Upload pem file failed"
                    else:
                        print "     Cannot find and click 'Install from' radio box"
                else:
                    print "     Cannot find and click Add btn"
            else:
                print "     Cannot find and click 'Trusted Certificates'"
            
            
            ############################################
            ########              LDAP Client Settings            #########
            ###########################################
            print "\n       Config LDAP Settings"
            element_des = "Click 'LDAP Client' link"
            element_name = ".//*[@id='lxca_core_widgets_detailsSelector_TextAbbr_2']/div"
            #element_name = "//div[contains(.,'LDAP Client')]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(2)
            
            
            element_des = "Checking Warning Dialog popup or not"
            element_name = ".//div[starts-with(@widgetid,'idx_widget_ModalDialog_')]"
            print "     " + str(element_des)
            if Is_element_exist(self, element_name , element_des):
                dialogs = self.driver.find_element_by_xpath(element_name)
                for dialog in range(len(dialogs)):
                    widgetid = 'idx_widget_ModalDialog_'+str(len(dialogs)-1-dialog);
                    self.driver.find_element_by_xpath("//div[@widgetid='"+widgetid+"']/div[@class='messageDialogFooter']/span[@class='messageAction']/span/span/span").click()
                    self.driver.implicitly_wait(30)
                    sleep(4)
            else:
                print "      Warning dialog do not pop up..."
                sys.stdout.flush()
            
            
            element_des = "Click 'Allow logons from LDAP users' Radio box"
            element_name = ".//*[@id='ldapClient_userAuthenticationMethod_RadioItem1']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(2)
                
                
            element_des = "Click 'Allow local users first, then LDAP users' Radio box"
            element_name = ".//*[@id='ldapClient_userAuthenticationMethod_RadioItem2']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(2)
            
            
            element_des = "Input LDAP Server IP"
            element_name = ".//*[@id='idx_form_TextBox_0']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys("10.243.2.230")
                self.driver.implicitly_wait(30)
                sleep(2)
                
                element_des = "Input LDAP Server Port"
                element_name = ".//*[@id='idx_form_TextBox_1']"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).clear()
                    self.driver.find_element_by_xpath(element_name).send_keys("636")
                    self.driver.implicitly_wait(30)
                    sleep(2)
                else:
                    print "     Can not find element and input AD server port"
            else:
                print "     Can not find element and input AD server IP"
            
            ##########
            element_des = "Input Client Name"
            element_name = ".//*[@id='ldapClient_clientDn']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys("CN=ccuser,CN=Users,DC=ad-aug,DC=aom,DC=net")
                self.driver.implicitly_wait(30)
                sleep(2)
                
                element_des = "Input Client PWD"
                element_name = ".//*[@id='ldapClient_clientPw']"
                if Is_element_exist(self, element_name , element_des):
                    self.driver.find_element_by_xpath(element_name).clear()
                    self.driver.find_element_by_xpath(element_name).send_keys("2Volley2")
                    self.driver.implicitly_wait(30)
                    sleep(2)
                else:
                    print "     Can not find element and input Client pwd"
            else:
                print "     Can not find element and input Client name"
            
            ###################
            element_des = "Input RootDN"
            element_name = ".//*[@id='ldapClient_rootDn']"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).clear()
                self.driver.find_element_by_xpath(element_name).send_keys("DC=ad-aug,DC=aom,DC=net")
                self.driver.implicitly_wait(30)
                sleep(2)
            else:
                print "     Can not find element and input RootDN"
                
            
            element_des = "Click 'Apply' button"
            element_name = "//span[contains(.,'Apply')]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(4)
            else:
                print "     Can not find element and input RootDN"
            
            
            element_des = "Click Close btn close dialog"
            element_name = ".//*[@class='messageDialogFooter']/span[3]/span[1]/span[1]/span[1]/span[3]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(2)
            else:
                print "     Can not click 'Close' button"
                
            
            element_des = "Click 'Return Initial Setup' return"
            element_name = ".//*[@id='lxca_core_widgets_detailsSelector_TextAbbr_13']/div"
            #element_name = "//span[contains(.,'Return to Initial Setup')]"
            if Is_element_exist(self, element_name , element_des):
                self.driver.find_element_by_xpath(element_name).click()
                self.driver.implicitly_wait(30)
                sleep(4)
            
        except Exception, e:
            print e
            scname = "Screenshot_Config_Service_And_Support_Settings.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            #self.assertEqual("Pass","Fail")
            raise unittest.SkipTest()
            #self.driver.close()
        
    ###############################################
    
    ###########Config  Start Managing Systems
    ###############################################
    def Config_Start_Managing_Systems(self):    
        #########   Config Start Managing Systems
        #####################
        print "\n7/8 - Start Managing Systems Config..."
        sys.stdout.flush()
        try:
            if "ipv6" in opt_job.lower():
                self.driver.get(ipv6_static_url)
            login_lxca(self)
            
            ############    Start to Management System
            #self.driver.find_element_by_xpath(".//*[@id='dijit__TemplatedMixin_6']/div[2]/div[3]").click()
            self.driver.find_element_by_xpath("//div[@class='setupStepTitle']//b[text()='Start Managing Systems']").click() 
            self.driver.implicitly_wait(30)
            sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='lxca_coreUI_initialSetup_InitialSetupDemoPage_0_initialSetupDemoExcludeDataNode']/span[1]/span[1]/span[1]").click()
            self.driver.implicitly_wait(30)
            sleep(10)
            
            print "      Config LXCA: '" + ipv4_static_ip + "' success..." 
            sys.stdout.flush()
            print "\n6/6 - Finished Management Systems..."
            sys.stdout.flush()
            
            try:
                self.driver.find_element_by_xpath(".//*[@id='_feedbackDialogNo_label']").click()
                #self.driver.find_element_by_xpath("//span[contains(.,'No thanks</')]").click()
                self.driver.implicitly_wait(30)
                sleep(2)
            except NoSuchElementException:
                print "Have not dialog 'Thank you for chossing Lenovo XClarity Administrator' pop up"
                sys.stdout.flush() 
             
        except Exception, e:
            print e
            scname = "Screenshot_Config_Start_Managing_Systems.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
            #self.driver.close()
    ###########################

    def LXCA_Wizard_state(self):
        print "\n8/8 - Start Managing Systems Config..."
        try:
            if "ipv6" in opt_job.lower():
                self.driver.get(ipv6_static_url)
                
            login_lxca(self)
            
            try:
                self.driver.find_element_by_xpath(".//*[@id='_feedbackDialogNo_label']").click()
                #self.driver.find_element_by_xpath("//span[contains(.,'No thanks</')]").click()
                self.driver.implicitly_wait(30)
                sleep(2)
            except NoSuchElementException:
                print "Have not dialog 'Thank you for chossing Lenovo XClarity Administrator' pop up when check 'LXCA_Wizard_state'"
                sys.stdout.flush() 
            
            self.driver.find_element_by_xpath(".//*[@id='hardware_text']").click()
            self.driver.implicitly_wait(30)
            sleep(4)
            
        except Exception, e:
            print e
            scname = "Screenshot_Get_LXCA_Wizard_state.jpg"
            self.driver.save_screenshot(scname)
            print "Screen captured: "+scname
            self.assertEqual("Pass","Fail")
    ###################################


    ################### 
    def tearDown(self):
        self.driver.close()
        
#######################

def run_suite_output_xml_report(suite, **args):
    descriptions = args.get('TEST_OUTPUT_DESCRIPTIONS', True)
    output_dir = args.get('TEST_OUTPUT_DESCRIPTIONS', '.')
    single_file = args.get('TEST_OUTPUT_FILE_NAME', 'LXCA_WIZARD.xml')
    kwargs = dict(verbosity=1, descriptions=descriptions, failfast=False)
    if single_file is not None:
        file_path = os.path.join(output_dir, single_file)
        with open(file_path, 'wb') as xml:
            return xmlrunner.XMLTestRunner(output=xml, **kwargs).run(suite)
    else :
        return xmlrunner.XMLTestRunner(output=output_dir, **kwargs).run(suite)
######################################

def generate_log():
    opt_url = ""
    jobname = opt_job
    if (len(sys.argv) > 3):
        opt_url = sys.argv[3]
    filelist = os.listdir(".")
    jpgfilelist = []
    for onefile in filelist:
        if (onefile.startswith("Screenshot") and onefile.endswith("jpg")):
            jpgfilelist.append(onefile)
    f = open("Screenshot.html","w")
    f.write("<html>")
    for onefile in jpgfilelist:
        f.write("<h1><a href=/"+jobname+"/"+opt_url+"/"+onefile+">"+onefile+"</a></h1>")
    f.write("</html>")
    f.close()

#############

if __name__ == "__main__":
    global current_path
    current_path = os.path.dirname(os.path.realpath(__file__))

    csv_file = 'vmlist.csv'
    lxca_user_wzd = "AUTOWZD"
    opt_job = sys.argv[1]
    
    config_txt = sys.argv[2]
    
    sys.stdout.flush()
    os.system("cls")
    print "#### Start time is: ", datetime.datetime.now()
    sys.stdout.flush()
    
    ########################
    get_lxca_info_from_config()
    
    ########################
    get_vmware_info_by_powershell()
    
    ########################
    get_lxca_info_from_csv()

    ipv6_url = "https://[" + ipv6_add + "]"    
    ipv4_static_url = "https://"+ipv4_static_ip+"/ui/index.html"
    ipv6_static_url = "https://["+ipv6_static_ip+"]/ui/index.html"
    ntp_server = "us.pool.ntp.org"
    print "Get eth1 IPv6 URL is: ", ipv6_url
    sys.stdout.flush()
    
    get_lxca_version_before_wzd(ipv6_url)
    testsuite = unittest.TestSuite()
    #testsuite.addTest(LXCA_Wizard("Add_Exception"))
    
    suite_arr = [
                    "License_Agreement", 
                    "Create_Multi_LXCA_Accounts", 
                    "Config_Network_Access", 
                    "Config_Date_and_Time", 
                    "Config_Service_and_Support_Settings", 
                    "Config_Additional_Security_Settings",
                    "Config_Start_Managing_Systems", 
                    "LXCA_Wizard_state"
                    ]
    for suite in suite_arr:
        testsuite.addTest(LXCA_Wizard(suite))
    
    """
    "License_2_Create_AUTOWZD", 
    "Create_Multi_LXCA_Accounts", 
    "Config_Network_Access", 
    "Config_Date_and_Time", 
    "Config_Service_and_Support_Settings", 
    "Config_Additional_Security_Settings",
    "Config_Start_Managing_Systems", 
    "LXCA_Wizard_state"
    """
    
    xml_file = "LXCA_WIZARD.xml"
    run_suite_output_xml_report(testsuite,TEST_OUTPUT_FILE_NAME=xml_file)
    #runner = unittest.TextTestRunner()
    #runner.run(testsuite)
    generate_log()
    os.system('taskkill /t /f -im chromedriver.exe')
    
