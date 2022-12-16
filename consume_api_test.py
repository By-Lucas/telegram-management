import requests

# 641639

def user_verification(contracti_id:int, email:str) -> None:
    url = 'http://127.0.0.1:8000/api/v1/eduzz/get_sale_list'

    data = {
        'start_date': '2020-12-03',
        'end_date': '2021-12-03',
        'contract_id': contracti_id ,
        'client_email': email
    }

    headers = {
            'Content-Type': 'application/json'
    }

    response = requests.request('GET', url=url, params=data, headers=headers)

    if response.json()['data'] != []:
        print(response.json())
        return response.json()

result = user_verification(966201, 'monica.liborio1@gmail.com')

if result is not None:
    print('Deu super certo', result['data'][0]['client_cel'], result['data'][0]['student_email'])

else:
    print('ERrorERrorERror')