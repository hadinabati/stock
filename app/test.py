import requests

a = requests.get('http://127.0.0.1:8000/openapi.json').json()
print(a)

