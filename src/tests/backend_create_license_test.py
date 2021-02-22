import requests

url = 'http://localhost:8012/create-license/'
data = {
    "admin-password": "admin123",
    "uses": 5
}

x = requests.post(url, json=data)

print(x.text)
