import requests
import base64

from dotenv import load_dotenv
import os
import sys
import json


load_dotenv(".env", encoding='utf-8')

URL_BASE = "https://api2.eduzz.com"
VERSION_API = "0.0.1-professional"

edduz_email = os.getenv('edduz_email')
api_key = os.getenv('edduz_public_key')
publick_key = os.getenv('edduz_api_key')

class Eduzz:

    def __init__(self, email, public_key, api_key):

        self.email = email
        self.public_key = public_key
        self.api_key = api_key

        self._headers = {
            'token': self.get_token(),
            'Content-Type': 'application/json'
        }

    def get_token(self):
        payload = {
            'email': self.email,
            'publickey': self.public_key,
            'apikey': self.api_key
        }

        try:
            response = requests.request('POST', url=f'{URL_BASE}/credential/generate_token', params=payload)
            data = response.json()

            return data['data']['token']

        except:
            return None

    async def get_sale_list(self, start_date, end_date, page=None, contract_id=None, affiliate_id=None,
                      content_id=None, invoice_status=None, client_email=None,
                      client_document=None, date_type=None):

        payload = {
            'start_date': start_date,
            'end_date': end_date
        }

        if page:
            payload['page'] = page
        if contract_id:
            payload['contract_id'] = contract_id
        if affiliate_id:
            payload['affiliate_id'] = affiliate_id
        if content_id:
            payload['content_id'] = content_id
        if invoice_status:
            payload['invoice_status'] = invoice_status
        if client_email:
            payload['client_email'] = client_email
        if client_document:
            payload['client_document'] = client_document
        if date_type:
            payload['date_type'] = date_type

        try:
            response = requests.request('GET', url=f'{URL_BASE}/sale/get_sale_list', headers=self._headers, params=payload)
            data = response.json()

            return data

        except:
            return None

    async def status_list(self):
        payload = {}

        try:
            response = requests.request('GET', url=f'{URL_BASE}/subscription/status_list/', headers=self._headers, params=payload)
            data = response.json()

            return data

        except Exception as e:
            print(e)
            return None

    async def get_contract_list(self, start_date, end_date, page):
        payload = {
            'page': page,
            'start_date': start_date,
            'end_date': end_date,
        }

        try:
            response = requests.request('GET', url=f'{URL_BASE}/subscription/get_contract_list', headers=self._headers, params=payload)
            data = response.json()

            return data

        except Exception as e:
            print(e)
            return None

    async def get_contract(self, contract_id: int, invoice_id: int):
        payload = {
            'contractId': contract_id,
            'invoiceId': invoice_id,
        }

        try:
            response = requests.request('GET', url=f'{URL_BASE}/subscription/get_contract/{contract_id}/invoices/{invoice_id}',
                                        headers=self._headers, params=payload)
            data = response.json()

            if data['data'][0]['status'] == 1:
                data['data'][0]['status'] = 'Ativo'
            if data['data'][0]['status'] == 2:
                data['data'][0]['status'] = 'Aguardando'
            if data['data'][0]['status'] == 3:
                data['data'][0]['status'] = 'Cancelado'
            if data['data'][0]['status'] == 4:
                data['data'][0]['status'] = 'Atrasado'
            if data['data'][0]['status'] == 5:
                data['data'][0]['status'] = 'Finalizado'
            if data['data'][0]['status'] == 6:
                data['data'][0]['status'] = 'Trial'
            if data['data'][0]['status'] == 7:
                data['data'][0]['status'] = 'Inadimplente'

            return data

        except Exception as e:
            print(e)
            return None


    async def get_total(self, start_date=None, end_date=None):
        '''formart of start_date and end_date: 2022-12-03'''

        payload = {
            'start_date': start_date,
            'end_date': end_date,
        }

        try:
            response = requests.request('GET',
                                        url=f'{URL_BASE}/sale/get_total',
                                        headers=self._headers, params=payload)
            data = response.json()
            return data

        except:
            return None
    
    async def get_balance(self):
        '''formart of start_date and end_date: 2022-12-03'''

        payload = {}

        try:
            response = requests.request('GET',
                                        url=f'{URL_BASE}/financial/balance',
                                        headers=self._headers, params=payload)
            data = response.json()
            return data

        except:
            return None


    async def content_list(self, page:int=None, active:int=None):

        payload = {
            'page': page,
            'active': active
        }

        try:
            response = requests.request('GET',
                                        url=f'{URL_BASE}/content/content_list',
                                        headers=self._headers, params=payload)
            data = response.json()
            return data

        except:
            return None
    
    async def get_content(self, content_id:int):

        payload = {}

        try:
            response = requests.request('GET',
                                        url=f'{URL_BASE}/content/content/{content_id}',
                                        headers=self._headers, params=payload)
            data = response.json()
            return data

        except:
            return None
