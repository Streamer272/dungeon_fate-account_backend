import requests

url = 'http://localhost:8012/register/'
data = {
    "username": "Streamer272",
    "password": "Daniel2308",
    "license_key": "12345-56789"
}

x = requests.post(url, json=data)

print(x.text)
