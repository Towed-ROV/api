from fastapi.responses import JSONResponse
import json


middl = {'index': 1100, 'payload_type': 'sensor_data', 'payload_data': [{'name': 'Temperature', 'value': 379.45}, {'name': 'Pressure', 'value': 2.09}, {'name': 'Variable', 'value': 0}]}

print(json.dumps(middl))
tuff = {"event": "data", "data": 123}

# print(JSONResponse(content=stuff).body)