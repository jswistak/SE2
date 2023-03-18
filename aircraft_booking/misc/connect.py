import requests

auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4OTIwOTM0LCJpYXQiOjE2Nzg5MTczMzQsImp0aSI6Ijg2N2UxNWNhZGVlNDRkOWQ4NWU4ZDhmZmI0Nzc5YzliIiwidXNlcl9pZCI6MX0.qqgtov0ehAabSNgZ4nr238s3OGrQ4vU739QHw-hgN2g'
hed = {'Authorization': 'Bearer ' + auth_token}
data = {'aircraft_id': 'SP-KOG',
        'aircraft_name': 'name', 'aircraft_type': "C182", 'aircraft_capacity': 4, 'aircraft_range': 1000, 'aircraft_speed': 100, 'aircraft_fuel': 100, 'aircraft_status': 'available', 'aircraft_cost_per_hour': 1000, 'aircraft_fuel_cost': 10}

url = 'http://localhost:8001/aircraft/'
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())
