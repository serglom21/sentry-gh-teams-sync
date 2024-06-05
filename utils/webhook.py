import hashlib
import hmac
import os
import json
from flask import request

def verify_signature(request):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        request: Flask request object
    
    print(request.data)
    secret_token = os.environ["GH_WEBHOOK_TOKEN"]
    signature_header = request.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
    if not signature_header:
        raise Exception("x-hub-signature-256 header is missing!")
    secret_token = secret_token.encode()
    expected_signature = hmac.HMAC(key=secret_token, msg=request.data, digestmod=hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature_header, expected_signature):
        raise Exception("Request signatures didn't match!")
    """
    signature_header = request.headers.get('X-Hub-Signature-256')
    secret_token = os.environ["GH_WEBHOOK_TOKEN"]
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    print(expected_signature)
    print(signature_header)
    if not hmac.compare_digest(expected_signature, signature_header):
        raise Exception("Request signatures didn't match!")
