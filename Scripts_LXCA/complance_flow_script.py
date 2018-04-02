import json, requests, time, warnings

warnings.filterwarnings('ignore')

condata = [
    '10.243.11.102',
    'USERID',
    'CME44ibm'
    ]

data = {"description":"Todd_Test_Solution","members":["nodes/214F5B00C3B111E0BEE15CF3FC6E2860"],"name":"Todd_Test_Solution","solutionVPD":{"console":"https://192.0.2.0","id":"59A54997C18DCF0594B8AAAA","machineType":"8695","manufacturer":"Lenovo","model":"AC1","serialNumber":"103D4F44"},"type":"solution"}


resouceGroup = requests.post('https://'+condata[0]+'/resourceGroups', auth=(condata[1],condata[2]), verify=False, json=data)
print(resouceGroup)

data = {"name":"powerRule","targetResources":[],"targetGroups":["/resourceGroups/59a54997c18dcf0594b8aaaa"],"targetResourceType":["Server"],"source":"inventory","content":[{"property":"powerStatus","ref_value":8}]}

createRule = requests.post('https://'+condata[0]+'/compliance/rules', auth=(condata[1],condata[2]), verify=False, json=data)

print(createRule.text)

data = {"solutionGroups" : ["59A54997C18DCF0594B8AAAA"]}

compositeResuls = requests.post('https://'+condata[0]+'/compliance/compositeResults', auth=(condata[1],condata[2]), verify=False, json=data)

respon = json.loads(str(compositeResuls.text))
compositeResulsId = respon[1][0]
print(compositeResulsId)


compResults = requests.get('https://'+condata[0]+'/compliance/compositeResults/'+compositeResulsId , auth=(condata[1],condata[2]) , verify = False)
print(compResults.text)
reData = json.loads(str(compResults.text))

result = reData[0]['results']

print(result)