import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from dotenv import load_dotenv
import os

load_dotenv(os.getcwd() + '\\.env', encoding='utf-8')


class SendEmail:

    def __init__(self) -> str:

        self.email_enviar = os.environ['email_send']
        self.senha_enviar = os.environ['email_password']
        

    def enviar_email(self,email: str, title_email: str, body: str) -> str:

        self.email_receber = email

        try:
            """
            A senha do email é gerada no link: https://security.google.com/settings/security/apppasswords
            """
            # Instância do MIMEMultipart
            msg = MIMEMultipart()
            msg['From'] = self.email_enviar
            msg['To'] = self.email_receber

            # Titulo da mensagem
            msg['Subject'] = title_email

            msg.attach(MIMEText(body, 'plain'))
            
            #Servidor SMTP
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.ehlo()
            # Segurança
            s.starttls()
            s.ehlo()
            s.login(self.email_enviar, self.senha_enviar)
            
            # Converte para String
            text = msg.as_string()

            s.sendmail(self.email_enviar, self.email_receber, text)
            print('Email enviado com sucesso!')
            s.quit()

        except Exception as e:
            print("O erro é =", e)