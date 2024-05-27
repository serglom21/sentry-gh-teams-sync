from request import request
from dotenv import load_dotenv
import os

class Sentry:

    def __init__(self):
        load_dotenv()
        self.api_token = os.environ["SENTRY_TOKEN"]

    def create_team_if_not_exists(self, team_slug):
        url = f'https://sentry.io/api/0/teams/tim-hortons/{team_slug}/'
        response = request(url, method = "GET", token = self.api_token)
        if response.status_code == 404: # team does not exist
            print(response.json())
            payload = {
                "slug" : team_slug
            }
            url = f'https://sentry.io/api/0/organizations/tim-hortons/teams/'
            response = request(url, method="POST", token = self.api_token, payload = payload)
            if response is not None and response.status_code == 200:
                print("team created succesfully")
                return True
            else:
                print("something went wrong")
                print(response.json())
                return False
        elif response.status_code == 200:
            print("team already created")
            return False

    def get_member_id_from_email(self, email):
        members = self.get_org_members()
        user_id = None
        for member in members:
            if "email" in member and member["email"] == email:
                user_id = member["id"]
        return user_id

    def get_org_members(self):
        url = 'https://sentry.io/api/0/organizations/tim-hortons/members/'
        response = request(url, method = "GET", token = self.api_token)
        members = []
        if response is not None and response.status_code == 200:
            members = members + response.json()
            next = response.links.get('next', {}).get('results') == 'true'
            while next:
                url = response.links.get('next', {}).get('url')
                response = request(url, method = "GET", token = self.api_token)
                next = response.links.get('next', {}).get('results') == 'true'
                data = response.json()
                members = members + data
            return members
        
        return None

    def add_member_to_team(self, member_id, team_slug):
        url = f'https://sentry.io/api/0/organizations/tim-hortons/members/{member_id}/teams/{team_slug}/'
        response = request(url, method = "POST", token = self.api_token)
        if response is not None and response.status_code in [200, 202, 204]:
            print(response.json())
            return True
        
        print("member could not be added")
        print(response.json())

    def delete_member_from_team(self, member_id, team_slug):
        url = f'https://sentry.io/api/0/organizations/tim-hortons/members/{member_id}/teams/{team_slug}/'
        response = request(url, method = "DELETE", token = self.api_token)
        if response is not None and response.status_code in [200]:
            print(response.json())
            return True
        
        print("member could not be deleted")
        print(response.json())


