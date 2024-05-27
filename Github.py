from request import request
from dotenv import load_dotenv
import os

class Github:
    def __init__(self):
        load_dotenv()
        self.api_token = os.environ["GH_TOKEN"]

    def get_email_from_login(self, user_login):
        url = f'https://api.github.com/users/{user_login}'
        response = request(url, method = "GET", token = self.api_token)
        if response is not None and response.status_code == 200:
            data = response.json()
            if "email" in data and data["email"] is not None:
                return data["email"]
        else:
            print(response.json())
            return None