import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('PROD_TOKEN')
base_url = os.getenv('PROD_URL')

# username = os.getenv('USERNAME')
# password = os.getenv('PASSWORD')
# user = {'username': username, 'password': password}
# r = requests.post(f'{base_url}/api-token-auth/', data=user)
# token = r.json()
# headers = {'Authorization': 'Token ' + token['token']}
# python manage.py drf_create_token mattcullenmeyer
headers = {'Authorization': 'Token ' + token}


def get(path, uid=''):
    url = f'{base_url}/api/v1/{path}/'
    if uid:
        url += f'{uid}/'

    r = requests.get(url, headers=headers)
    data = r.json()

    if uid:
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    return df


def post(path, data):
    r = requests.post(f'{base_url}/api/v1/{path}/', data=data, headers=headers)
    return r


def put(path, uid, data):
    r = requests.put(f'{base_url}/api/v1/{path}/{uid}/', data=data, headers=headers)
    return r


def delete(path, uid):
    r = requests.delete(f'{base_url}/api/v1/{path}/{uid}/', headers=headers)
    return r
