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
    
    """
    signature_header = request.headers.get('X-Hub-Signature-256')
    secret_token = os.environ["GH_WEBHOOK_TOKEN"]
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise Exception("Request signatures didn't match!")
