from Sentry import Sentry
from Github import Github
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
            if "team" in data and "slug" in data["team"]:
                response = sentry.create_team_if_not_exists(data["team"]["slug"])
                print(f'team created: {response}')
            else:
                return jsonify({'status': 'failed', 'message': 'No team slug provided'}), 502

        if (data["action"] == "deleted"):
            if "team" in data and "slug" in data["team"]:
                response = sentry.delete_team_if_exists(data["team"]["slug"])
                print(f'team deleted: {response}')
            else:
                return jsonify({'status': 'failed', 'message': 'No team slug provided'}), 502

        if (data["action"] == "added" and data["scope"] == "team"):
            if "member" in data and "login" in data["member"]:
                email = github.get_email_from_login(data["member"]["login"])
                member_id = sentry.get_member_id_from_email(email)
                if "team" in data and "slug" in data["team"]:
                    response = sentry.add_member_to_team(member_id, data["team"]["slug"])
                    print(f'member added: {response}')
                else:
                    return jsonify({'status': 'failed', 'message': 'No team slug provided'}), 502
            else:
                return jsonify({'status': 'failed', 'message': 'No member login provided'}), 502

        if (data["action"] == "removed" and data["scope"] == "team"):
            email = github.get_email_from_login(data["member"]["login"])
            member_id = sentry.get_member_id_from_email(email)
            response = sentry.delete_member_from_team(member_id, data["team"]["slug"])
            print(f'member deleted: {response}')
        else:
            return jsonify({'status': 'failed', 'message': 'No member login provided'}), 502
        
        return jsonify({'status': 'success'}), 200
    except Exception as error:
        print(error)
        return jsonify({'status': 'failed', 'message': str(error)}), 502

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(host='0.0.0.0', port=5500)