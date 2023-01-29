import base64
import hashlib
import hmac
import json
import os
import time
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

URL_API = os.getenv('URL_API')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
URL_INTERNAL = os.getenv('URL_INTERNAL')
LOGIN = '/login'


class API_auth:
    @staticmethod
    def login_user(USERNAME, PASSWORD, domain_origin):
        ''' This is the login endpoint. Pass in the user credentials to sign in. Returns a json response.
                If you are testing the actual endpoint and want to return the status code and json response, pass in bearer_only=0'''
        endpoint = f'{URL_API}{LOGIN}'
        req_body = {
            "username": USERNAME,
            "password": PASSWORD
        }
        headers = {
            'Origin': f'{URL_INTERNAL}'
        }
        response = requests.post(url=endpoint, json=req_body, headers=headers, timeout=360)
        json_response = json.loads(response.content)

        return json_response

    def get_auth_headers(self, user: str, password: str, endpoint: str, request_method: str, request_body=None):
        ''' Retrieves the authorisation headers required to authenticate an API request. This is a requirement for HMAC. '''
        timestamp = int(time.time())
        endpoint = endpoint.replace('https://', '').replace('http://', '').replace('://', '')
        nonce = 1
        user = self.login_user('2011guptashalini@gmail.com', "Purply@1234", domain_origin='https://testing.purplyapp.com')
        if request_body is None:
            request_body = ''
        else:
            # Convert it to string and change quotes to match server side.
            request_body = json.dumps(request_body)
        mac_string = f'{timestamp} {nonce} {request_method} {endpoint} {request_body}'
        signature = base64.b64encode(hmac.new(str(user['secretKey']).encode('utf-8'), mac_string.encode('utf-8'), hashlib.sha256).digest())
        return {
            'Authorization': 'Bearer ' + user['token'],
            'mac': signature.decode(),
            'nonce': str(nonce),
            'timestamp': str(timestamp)
        }
