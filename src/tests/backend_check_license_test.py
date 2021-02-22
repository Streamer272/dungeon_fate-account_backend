import requests

url = 'http://localhost:8012/check-license/'
data = {
    "license_key": "12345-56789"
}

x = requests.post(url, json=data)

print(x.text)
