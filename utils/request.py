import requests

def request(url, method, token, payload = None):
    try:
        headers = {
                "Content-Type": "application/json",
                "Authorization" : f'Bearer {token}'
            }
        if method == "GET":
            return requests.get(url, headers = headers)
        elif method == "POST":
            return requests.post(url, json = payload, headers = headers)
        elif method == "PUT":
            return requests.put(url, json = payload, headers = headers)
        elif method == "DELETE":
            return requests.delete(url, headers = headers)
    except Exception as e:
        raise Exception(f'Could not make request to {url} - Reason: {str(e)}')
