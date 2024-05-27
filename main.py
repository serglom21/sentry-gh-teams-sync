from Sentry import Sentry
from Github import Github
from flask import Flask, request

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
            response = sentry.create_team_if_not_exists(data["team"]["slug"])
            print(f'team created: {response}')

        if (data["action"] == "added" and data["scope"] == "team"):
            email = github.get_email_from_login(data["member"]["login"])
            member_id = sentry.get_member_id_from_email(email)
            response = sentry.add_member_to_team(member_id, data["team"]["slug"])
            print(f'member added: {response}')

        if (data["action"] == "removed" and data["scope"] == "team"):
            email = github.get_email_from_login(data["member"]["login"])
            member_id = sentry.get_member_id_from_email(email)
            response = sentry.delete_member_from_team(member_id, data["team"]["slug"])
            print(f'member deleted: {response}')
    except Exception as error:
        print(error)

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(host='0.0.0.0', port=5500)