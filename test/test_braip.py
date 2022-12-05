import os
from datetime import datetime, timedelta

import pytest
import requests

from dotenv import load_dotenv

from core.plataforms.braip import Braip

load_dotenv()

# BRAIP
token_braip = os.getenv("token_braip")


def test_token():
    token_braip = os.getenv("token_braip")
    assert len(token_braip) == 1086


def test_braip_class():
    braip_class = Braip("token")
    assert braip_class is not None


def test_braip_connection():
    request_connection = requests.get("https://ev.braip.com/api/vendas")
    assert request_connection.status_code == 200


# def braip_request_api():
#     token = os.getenv('token_braip')
#     request_braip_api = requests.get(url='https://ev.braip.com/api/vendas',
#                                      headers={'Authorization': 'Bearer ' + token},
#                                      params={'product_key': 'product_key', 'transaction_key': 'transaction_key'})
#     print(request_braip_api.json())
#     return request_braip_api.status_code


def test_get_transactions(product_key=None, transaction_key=None, date_min=None,
                          date_max=None, last_update_min=None, last_update_max=None, status=None,
                          payment=None, page=None, participation=None
                          ):
    method_url = 'https://ev.braip.com/api/vendas'
    headers = {'Authorization': 'Bearer ' + token_braip}
    payload = {}

    if product_key:
        payload['product_key'] = product_key
    if transaction_key:
        payload['transaction_key'] = transaction_key
    if date_min:
        payload['date_min'] = date_min
    else:
        date = datetime.now() - timedelta(180)
        date_min = date.strftime('%Y-%m-%d %H:%I:%S')
        payload['date_min'] = date_min
    if date_max:
        payload['date_max'] = date_max
    else:
        date = datetime.now()
        date_max = date.strftime('%Y-%m-%d %H:%I:%S')
        payload['date_max'] = date_max
    if last_update_min:
        payload['last_update_min'] = last_update_min
    if last_update_max:
        payload['last_update_max'] = last_update_max
    if status:
        payload['status'] = status
    if payment:
        payload['payment'] = payment
    if page:
        payload['page'] = page
    if participation:
        payload['participation'] = participation

    r = requests.get(url=method_url, headers=headers, params=payload)
    data = r.json()
    assert data is not None
