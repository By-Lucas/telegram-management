import os
import requests

from dotenv import load_dotenv

load_dotenv()


def braip_connection():
    request_connection = requests.get("https://ev.braip.com/api/vendas")
    return request_connection.status_code


def test_braip_connection():
    assert braip_connection() == 200


def braip_request_api():
    token = os.getenv('token_braip')
    request_braip_api = requests.get(url='https://ev.braip.com/api/vendas',
                                     headers={'Authorization': 'Bearer ' + token},
                                     params={'product_key': 'product_key', 'transaction_key': 'transaction_key'})
    print(request_braip_api.json())
    return request_braip_api.status_code


def test_braip_request_api():
    assert braip_request_api() == 200


if __name__ == '__main__':
    brt = braip_request_api()
    print(brt)
