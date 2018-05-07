import requests, warnings, openpyxl, os
from openpyxl.styles import Font, Alignment, colors, Border, Side, Style

warnings.filterwarnings('ignore')
global key, bz
key='AirXEelVqsNtHp4I3OwavnZpVBcG5OdaKf8zuU0S'
bz='https://bz.labs.lenovo.com'

def getBugList():
    fullBugList =[]
    search=requests.get(bz+'/rest/bug?bug_status=Open&bug_status=Working&bug_status=Rejected&product=CMM&product=DSA&product=LXCE_BoMC&product=LXCE_OneCLI&product=LXCE_UpdateXpress&product=LXCI&product=SCOM&product=SCVMM&product=XClarity%20Administrator&resolution=---&api_key='+key,verify=False)
    for bug in search.json()['bugs']:
        fullBugList.append(bug['id'])
        
    
    return fullBugList

def checkBugHistory(buglist):
    rejCount = 0
    suspectBugList=[]
    for bug in buglist:
        #print('\n')
        print('******************Checking Bug #'+str(bug)+' now!****************************')
        search=requests.get(bz+'/rest/bug/'+str(bug)+'/history?&api_key='+key,verify=False)
        for change in search.json()['bugs'][0]['history']:
            for r in change['changes']:
                if r['field_name'] == 'status' and r['added'] == 'Rejected':
                    #print('     Feid name is '+r['field_name'] + ' and '+r['added']+' was added')
                    rejCount = rejCount + 1
                    #print('    Count is '+str(rejCount))
                    if rejCount >2:
                        suspectBugList.append(bug)
                        rejCount = 0
                        #print('        '+str(rejCount)+ ' should be Zero now')
        #print('*****Done with Bug# '+str(bug)+' counter is '+str(rejCount)+' Setting counter back to zero now*****')
        #print('\n')
        rejCount = 0
                        
    return suspectBugList
                        
                
def createReport(badBuglist):
    try:
        os.remove('Reject_Report.xlsx')
    except Exception as ex:
        print(ex)
        
    print('generating report now')
    hFont=Font(name='Calibri(body)', size=13, bold=True, color=colors.BLUE)
    hBorder = Border(bottom=Side(style='thick',color=colors.BLACK))
    hAlignment = Alignment(horizontal='center')
    header = Style(font = hFont, border=hBorder, alignment=hAlignment)
    rowCount = 2
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Overly_Rejected_Bugs'
    sheet['A1'] = 'Bugid'
    sheet['B1'] = 'Summary'
    sheet['C1'] = 'Bug Status'
    sheet['D1'] = 'Product'
    sheet['E1'] = 'Release'
    sheet['F1'] = 'Reporter'
    sheet['G1'] = 'Current Owner'
    sheet['A1'].style = header
    sheet['B1'].style = header
    sheet['C1'].style = header
    sheet['D1'].style = header
    sheet['E1'].style = header
    sheet['F1'].style = header
    sheet['G1'].style = header
    for bug in badBuglist:
        search=requests.get(bz+'/rest/bug/'+str(bug)+'?&api_key='+key,verify=False)
        sheet['A'+str(rowCount)].value = search.json()['bugs'][0]['id']
        sheet['A'+str(rowCount)].hyperlink = 'https://bz.labs.lenovo.com/show_bug.cgi?id='+str(bug)
        sheet['A'+str(rowCount)].font= Font(color=colors.BLUE)
        sheet['B'+str(rowCount)] = search.json()['bugs'][0]['summary']
        sheet['C'+str(rowCount)] = search.json()['bugs'][0]['status']
        sheet['D'+str(rowCount)] = search.json()['bugs'][0]['product']
        sheet['E'+str(rowCount)] = search.json()['bugs'][0]['version']
        sheet['F'+str(rowCount)] = search.json()['bugs'][0]['creator']
        sheet['G'+str(rowCount)] = search.json()['bugs'][0]['assigned_to']
        rowCount = rowCount + 1
    wb.save('c:\\pydata\\reports\\Reject_Report.xlsx')
    

list1 = getBugList()
badBuglist = checkBugHistory(list1)
createReport(badBuglist)