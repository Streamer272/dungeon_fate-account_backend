import requests

url = 'http://localhost:8012/login/'
data = {
    "username": "Streamer272",
    "password": "Daniel2308"
}

x = requests.post(url, json=data)

print(x.text)
