import requests

import configparser

from dotenv import load_dotenv
import os

diretorio = os.getcwd() #Pega o diretório atual
num = diretorio.rfind("\\") + 1 #Acha onde tem a ultima "\"
os.chdir(diretorio[:num]) #Volta o diretório

load_dotenv(".env",encoding='utf-8')

print(os.environ['name_bot'])



class TelegramManagement:
    def __init__(self) -> None:
        super().__init__()

        self.headers = {}


    def _requests(self, method:str, url_api:str ,data:dict):

        if method == 'GET':
            response = requests.request(method=method, url=url_api, data=data, headers=self.headers)