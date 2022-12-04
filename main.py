from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

from dotenv import load_dotenv
import os

load_dotenv(os.getcwd() + '\\.env', encoding='utf-8')

title= os.getenv('title')
description = 'Gerenciar usuários do grupo telegram telegram de acordo com status de cada usuário nas plataformas de Marketplace: Eduzz, Braip, Hotmart, Kiwify e TK Global (Plataforma própria)'
version= os.getenv('version')

app = FastAPI(title= title, 
            description= description,
            version= version)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

    """
    token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjY2NzIxMTEzLCJpYXQiOjE2NjYxMTYzMTMsInN1YiI6IjEifQ.NeSxX-U9eNYNg88rkBEMx4VCS4XMRP4Z2f4tx-adLBE
    tipo: bearer 
    """