import httpx
import json


access_token = '0123456789abcdef0123456789abcdef01234567'
headers = {
    'Authorization': f"Token {access_token}",
    'Content-Type': 'application/json',
    'Accept': 'application/json; indent=4'
}

# manufacturers
data = {
    "name": "Juniper",
}
response = httpx.post('http://localhost:8080/api/dcim/manufacturers/', headers = headers, json = data)
print(response.json())


# session_params = {
#   "count": 0,
#   "results": [
#     {
#       "name": "Juniper",
#     }
#   ]
# }
# response = httpx.get('http://localhost:8080/api/dcim/manufacturers/', headers = headers, params = session_params)
manufacturers_id = dict()
response = httpx.get('http://localhost:8080/api/dcim/manufacturers/', headers = headers)
for result in (response.json())['results']:
    manufacturers_id[result['name']] = result['id']
print(manufacturers_id)

# device-roles
response = httpx.get('http://localhost:8080/api/dcim/device-roles/', headers = headers, params = session_data)

session_data = {
  "name": "Router",
}
response = httpx.post('http://localhost:8080/api/dcim/device-roles/', headers = headers, json = session_data)
print("device-roles", response.text)


# device-types
session_data = {
  "manufacturer": "8ffb0870-941d-462b-ae0a-405ad289c1c9",  
  "model": "MX80",
  "custom_fields": {}
}
# session_data = {
#   "manufacturer": {
#     "name": "Juniper",
#   },
#   "model": "MX80",
# }
response = httpx.post('http://localhost:8080/api/dcim/device-types/', headers = headers, json = session_data)
print("device-types", response.text)


# sites
session_data = {
  "name": "Ekaterinburg",
  "status": "active",
}
response = httpx.post('http://localhost:8080/api/dcim/sites/', headers = headers, json = session_data)
print("sites", response.text)


# devices
session_data = {
  "name": "RN-Ekaterinburg-RT1",
  "device_type": {
    "manufacturer": {
      "id": "8ffb0870-941d-462b-ae0a-405ad289c1c9", 
      "name": "Juniper",
    },
    "model": "MX80",

  },
  "device_role": {
    "id": "7396faa3-ffc2-45b5-81b8-8606ee71aac4",
    "name": "Router",
  },
  "status": "active",
  "site": {
    "id": "9b7eff82-25a6-43c9-8740-6df53811d57c",    
    "slug": "ekaterinburg",
    "name": "Ekaterinburg",
  },
}
response = httpx.post('http://localhost:8080/api/dcim/devices/', headers = headers, json = session_data)
print("devices", response.text)


