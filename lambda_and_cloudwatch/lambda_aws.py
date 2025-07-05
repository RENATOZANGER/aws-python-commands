import base64
import json
import hmac
import hashlib
import time

""" Example of creating a JWT (JSON Web Token) in Python for use with AWS Lambda. """


def base64url_encode(data):
    """ Encode bytes to base64-url without padding. """
    
    return base64.urlsafe_b64encode(data).rstrip(b'=')

def create_jwt(payload, secret, algorithm='HS256'):
    """ Create a JSON Web Token (JWT) signed with HMAC SHA-256. """
    
    header = {
        'alg': algorithm,
        'typ': 'JWT'
    }

    # Encode header and payload
    header_json = json.dumps(header, separators=(',', ':')).encode()
    payload_json = json.dumps(payload, separators=(',', ':')).encode()

    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload_json)

    signing_input = header_b64 + b'.' + payload_b64

    # Create signature
    if algorithm == 'HS256':
        signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    else:
        raise ValueError('Algoritmo não suportado')

    signature_b64 = base64url_encode(signature)

    jwt_token = b'.'.join([header_b64, payload_b64, signature_b64])
    return jwt_token.decode()


def lambda_handler(event, context):
    """ AWS Lambda handler function to create a JWT token. """
    
    secret = 'my-secret-key'
    now = int(time.time())
    payload = {
        'sub': '12345', # User ID
        'iat': now,
        'exp': now+ 30  # expires in 30 seconds
    }

    token = create_jwt(payload, secret)
    print(f"Token:{token}")
    
    return {
        'statusCode': 200,
        'Token': token
    }
