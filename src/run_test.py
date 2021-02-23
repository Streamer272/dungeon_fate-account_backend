import unittest
import requests

backend_url = "http://localhost:8012/"


def send_request(url: str, data: dict) -> int:
    request = requests.post(backend_url + url, json=data)

    return request.status_code


class BackendTest(unittest.TestCase):
    def test_register(self):
        self.assertEqual(
            send_request(
                "register/",
                {
                "username": "Streamer272enemy",
                "password": "Daniel2308",
                "license_key": "12345-56789"
                }
            ),
            200
        )

    def test_login(self):
        self.assertEqual(
            send_request(
                "login/",
                {
                "username": "Streamer272",
                "password": "Daniel2308"
                }
            ),
            200
        )

    def check_license(self):
        self.assertEqual(
            send_request(
                "check-license/",
                {
                "license_key": "12345-56789"
                }
            ),
            200
        )

    def create_license(self):
        self.assertEqual(
            send_request(
                "create-license/",
                {
                "admin-password": "admin123",
                "uses": 5
                }
            ),
            200
        )


if __name__ == '__main__':
    unittest.main()
