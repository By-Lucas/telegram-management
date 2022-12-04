import os
import requests

from datetime import datetime, timedelta

from dotenv import load_dotenv


class Braip:
    def __init__(self, token):
        self.token = token

    def get_transactions(self, product_key=None, transaction_key=None, date_min=None,
                         date_max=None, last_update_min=None, last_update_max=None, status=None,
                         payment=None, page=None, participation=None):

        method_url = 'https://ev.braip.com/api/vendas'
        headers = {'Authorization': 'Bearer ' + self.token}
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

        try:
            r = requests.get(url=method_url, headers=headers, params=payload)
            print(r.status_code)
            data = r.json()
            return data
        except:
            return None


if __name__ == '__main__':
    load_dotenv()
    token_braip = os.getenv('token_braip')
    braip_ = Braip(token=token_braip)
    response = braip_.get_transactions()
    print(response)
