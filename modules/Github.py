from utils.request import request
from dotenv import load_dotenv
from utils.responses.GithubResponse import GithubResponse
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
            if "email" not in data or data["email"] is None or data["email"] == "":
                return GithubResponse(502, f'Could not find email for login: {user_login}')
            
            return GithubResponse(200, "Email retrieved successfully", data["email"])
        
        return GithubResponse(502, f'Could not find email for login: {user_login}')
