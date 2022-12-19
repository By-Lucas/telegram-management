import requests
import json

# 641639

url = 'http://127.0.0.1:8000/api/v1'

def user_verification(contracti_id:int, email:str) -> None:
   

    data = {
        'start_date': '2020-12-03',
        'end_date': '2021-12-03',
        'contract_id': contracti_id ,
        'client_email': email
    }

    headers = {
            'Content-Type': 'application/json'
    }

    response = requests.request('GET', url=f'{url}/eduzz/get_sale_list', params=data, headers=headers)

    if response.json()['data'] != []:
        print(response.json())
        return response.json()

# result = user_verification(966201, 'monica.liborio1@gmail.com')

# if result is not None:
#     print('Deu super certo', result['data'][0]['client_cel'], result['data'][0]['student_email'])

# else:
#     print('ERrorERrorERror')


def get_user(email:str):
        headers = {
                'Content-Type': 'application/json'
        }
        response = requests.request('GET', url=f'{url}/user/{email}', headers=headers)

        if response.status_code == 200:
            return response.json()

# result = get_user(email='lucas@gmail.com')
# print(result)


def new_user():
   
    try:
        payload = {
            'id': 20,
            "full_name": "Lucas Silva",
            "birth_date": "string",
            "phone": "string",
            "cpf": "string",
            "email": 'user@example.com',
            "is_admin": False,
            "password": "string"
            }

        data = {
        "username": "@lucasSilva",
        "telegram_id": int(1561000),
        "url_fonte": "string.com.br",
        "id": 20
        }

        params= {
            "user_id": 20
         }

        headers = {
            'Content-Type': 'application/json'
        }

        
        #response = requests.request('POST', url=f'{url}/user/signup',data=json.dumps(payload), headers=headers)
        response2 = requests.request('POST', url=f'{url}/user/info-telegram',data=json.dumps(data), headers=headers)


        return response2
    except Exception as e:
        print(e)


response = new_user()
print(response.content)