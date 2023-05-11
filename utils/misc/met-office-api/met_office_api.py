# import requests

# url = 'https://api-metoffice.apiconnect.ibmcloud.com/v0/forecasts/point/hourly?excludeParameterMetadata=False&includeLocationName=False&latitude=51.5654&longitude=0.1349'

# params = {'X-IBM-Client-Id': '<id>',
#           'X-IBM-Client-Secret': '<secret>', 
#           'accept' : 'application/json'}

# response = requests.get(url, params=params)

# print(response)

# Documentation here: https://metoffice.apiconnect.ibmcloud.com/metoffice/production/product/30315/api/30309#/Globalhourlyspotdata_102/operation/%2Fforecasts%2Fpoint%2Fhourly/get

# curl --request GET \
#   --url 'https://api-metoffice.apiconnect.ibmcloud.com/v0/forecasts/point/hourly?excludeParameterMetadata=False&includeLocationName=False&latitude=REPLACE_THIS_VALUE&longitude=REPLACE_THIS_VALUE' \
#   --header 'X-IBM-Client-Id: <id>' \
#   --header 'X-IBM-Client-Secret: <secret>' \
#   --header 'accept: application/json'


import http.client
import json


conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

headers = {
    'X-IBM-Client-Id': "<id>",
    'X-IBM-Client-Secret': "<secret>",
    'accept': "application/json"
    }

conn.request("GET", "/v0/forecasts/point/hourly?excludeParameterMetadata=False&includeLocationName=False&latitude=51.5654&longitude=0.1349", headers=headers)

res = conn.getresponse()
data = res.read()

res_json = json.loads(data.decode("utf-8"))

with open('json_data.json', 'w') as outfile:
    json.dump(res_json, outfile, sort_keys=True, indent=4)

# print(json.dumps(res_json, sort_keys=True,indent=4))




