import json
import os

from products.AdvertisePurple.utils.api_auth import API_auth


import requests
USERNAME = '2011guptashalini@gmail.com'
PASSWORD = 'Purply@1234'
ENDPOINT_LOGIN = 'https://services.testing.purplyapp.com/login'


def test_login_internal_success_200(api_setup):
    '''
    Endpoint : /login
    type: POST
    Status code: 200
    '''
    # Setup
    api_auth_obj = API_auth()
    endpoint = ENDPOINT_LOGIN
    req_body = {
        'username': USERNAME,
        'password': PASSWORD
    }
    req_headers = api_auth_obj.get_auth_headers(USERNAME, PASSWORD, endpoint, 'POST', req_body)
    # Execute
    response = requests.post(url=endpoint, headers=req_headers, json=req_body, timeout=60)
    response_body = json.loads(response.content)
    # Assert
    assert response.status_code == 200
