from modules.Sentry import Sentry
from modules.Github import Github
from utils.exceptions.MissingParametersException import MissingParametersException
from utils.responses.HTTPResponse import HTTPResponse
from utils.responses.GithubResponse import GithubResponse
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=["GET"])
def check_health():
    return "server is healthy"

@app.route('/github', methods=["POST"])
def github_webhook_post():
    try:
        data = request.get_json()
        sentry = Sentry()
        github = Github()
        if (data["action"] == "created"):
            validate_params(data, "team", "slug")
            
            response = sentry.create_team_if_not_exists(data["team"]["slug"])
            return handle_response(response)

        if (data["action"] == "deleted"):
            validate_params(data, "team", "slug")
            
            response = sentry.delete_team_if_exists(data["team"]["slug"])    
            return handle_response(response)

        if (data["action"] == "added" and data["scope"] == "team"):
            validate_params(data, "member", "login")
            validate_params(data, "team", "slug")

            email_response = github.get_email_from_login(data["member"]["login"])
            email = None
            if isinstance(email_response, GithubResponse):
                if email_response.get_status_code() not in [200,202,204]:
                    raise Exception(f'Could not find github email for login: {data["member"]["login"]}')
                else:
                    email = email_response.get_data()
            else:
                raise Exception('Invalid response')
            
            member_id = sentry.get_member_id_from_email(email)
            response = sentry.add_member_to_team(member_id, data["team"]["slug"])
            return handle_response(response)
                
        if (data["action"] == "removed" and data["scope"] == "team"):
            validate_params(data, "member", "login")
            validate_params(data, "team", "slug")

            email_response = github.get_email_from_login(data["member"]["login"])
            email = None
            if isinstance(email_response, GithubResponse):
                if email_response.get_status_code() not in [200,202,204]:
                    raise Exception(f'Could not find github email for login: {data["member"]["login"]}')
                else:
                    email = email_response.get_data()
            else:
                raise Exception('Invalid response')
            
            member_id = sentry.get_member_id_from_email(email)
            response = sentry.delete_member_from_team(member_id, data["team"]["slug"])
            return handle_response(response)
            
    except Exception as error:
        return jsonify({'status': 'failed', 'message': str(error)}), 502

def validate_params(data, param1, param2 = None):
    if param2 == None:
        if param1 not in data:
            raise MissingParametersException(f'No {param1} provided')
        if data[param1] is None or data[param1] == "":
            raise MissingParametersException(f'Invalid format for {param1}')
    else:
        if param1 not in data or param2 not in data[param1]:
            raise MissingParametersException(f'No {param1} {param2} provided')
            
        if data[param1][param2] is None or data[param1][param2] == "":
            raise MissingParametersException(f'Invalid value for {param1} {param2}')

    return True

def handle_response(response):
    if isinstance(response, HTTPResponse):
        if response.get_status_code() in [200,202,204]:
            return jsonify({'status': 'success', 'message': response.get_message()}), 200
        else:
            return jsonify({'status': 'failed', 'message': response.get_message()}), 200

    return jsonify({'status': 'failed', 'message': 'An unknown error happened'}), 502


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(host='0.0.0.0', port=5500)