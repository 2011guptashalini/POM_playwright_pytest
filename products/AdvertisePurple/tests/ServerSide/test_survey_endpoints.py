
import json

import pymysql
import requests

from products.AdvertisePurple.utils import utils as util
from products.AdvertisePurple.utils.api_auth import API_auth


ENDPOINT_SURVEY = 'https://services.testing.purplyapp.com/affiliates/'
USERNAME = '2011guptashalini@gmail.com'
PASSWORD = 'Purply@1234'
ENDPOINT_LOGIN = 'https://services.testing.purplyapp.com/login'
SURVEY='/survey'


def test_survey_success_200(api_setup) -> None:
    '''
    Endpoint : /SurveyID/survey
    type: POST
    Status code: 200
    '''
    # finding affiliate id from DB
    # AP_MYSQL.connect_db()
    cur = api_setup
    sql_query_affiliate_id = f'''select id from affiliates where name = '{util.AFFILIATE_NAME}';'''
    cur.execute(sql_query_affiliate_id)
    result = cur.fetchone()
    affiliate_id = result[0]
    # AP_MYSQL.disconnect_db()
    # Setup
    api_auth_obj = API_auth()
    endpoint = f'{ENDPOINT_SURVEY}{affiliate_id}{SURVEY}'
    req_body = {
        'username': USERNAME,
        'password': PASSWORD
    }
    req_headers = api_auth_obj.get_auth_headers(USERNAME, PASSWORD, ENDPOINT_LOGIN, 'POST', req_body)
    # Execute
    response = requests.get(url=endpoint, headers=req_headers, timeout=60)
    response_body = json.loads(response.content)
    # Assert
    assert response.status_code == 200
    assert response_body['affiliateProfile']['affiliateCorporateName'] == 'Test Corporate Name'
