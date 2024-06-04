from utils.request import request
from dotenv import load_dotenv
from utils.responses.HTTPResponse import HTTPResponse
import os

class Sentry:

    def __init__(self):
        load_dotenv()
        self.api_token = os.environ["SENTRY_TOKEN"]
        self.org_slug = os.environ["SENTRY_ORG_SLUG"]

    def create_team_if_not_exists(self, team_slug):
        url = f'https://sentry.io/api/0/teams/{self.org_slug}/{team_slug}/'
        response = request(url, method = "GET", token = self.api_token)
        if response.status_code == 404: # team does not exist
            payload = {
                "slug" : team_slug
            }
            url = f'https://sentry.io/api/0/organizations/{self.org_slug}/teams/'
            response = request(url, method="POST", token = self.api_token, payload = payload)
            if response is not None and response.status_code in [200,201,202,204]:
                return HTTPResponse(200, "Team created successfully")
            else:
                return HTTPResponse(response.status_code, "Team could not be created")
        elif response.status_code == 200:
            return HTTPResponse(200, "Team already exists")
        
    def delete_team_if_exists(self, team_slug):
        url = f'https://us.sentry.io/api/0/teams/{self.org_slug}/{team_slug}/'
        response = request(url, method = "DELETE", token = self.api_token)
        if response.status_code in [200,201,202,204]:
            return HTTPResponse(200, f'Team {team_slug} deleted successfully')
        
        return HTTPResponse(502, f'Team {team_slug} could not be deleted')

    def get_member_id_from_email(self, email):
        members = self.get_org_members()
        user_id = None
        for member in members:
            if "email" in member and member["email"] == email:
                user_id = member["id"]
        return user_id

    def get_org_members(self):
        url = f'https://sentry.io/api/0/organizations/{self.org_slug}/members/'
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
        url = f'https://sentry.io/api/0/organizations/{self.org_slug}/members/{member_id}/teams/{team_slug}/'
        response = request(url, method = "POST", token = self.api_token)
        if response is not None and response.status_code in [200, 201, 202, 204]:
            return HTTPResponse(response.status_code, "Member added successfully")
        
        return HTTPResponse(response.status_code, f'Member {member_id} could not be added to team: {team_slug}')


    def delete_member_from_team(self, member_id, team_slug):
        url = f'https://sentry.io/api/0/organizations/{self.org_slug}/members/{member_id}/teams/{team_slug}/'
        response = request(url, method = "DELETE", token = self.api_token)
        if response is not None and response.status_code in [200]:
            return HTTPResponse(200, f'Member {member_id} deleted successfully from team {team_slug}')
        
        return HTTPResponse(response.status_code, f'Member {member_id} could not be deleted from team: {team_slug}')


