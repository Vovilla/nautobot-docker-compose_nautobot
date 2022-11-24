import httpx


session = httpx.Client()
access_token = '0123456789abcdef0123456789abcdef01234567'
session.headers.update({'Authorization': f"Token {access_token}"})
session.headers.update({'Accept': 'application/json; indent=4'})
session_data = {
    "name": "Juniper",
}
response = session.post('http://localhost:8080/api/dcim/manufacturers/', data = session_data)
print(response.text)

session_params = {
  "count": 0,
  "results": [
    {
      "name": "Juniper",
    }
  ]
}
response = session.get('http://localhost:8080/api/dcim/manufacturers/', params = session_params)
print(response.text)
