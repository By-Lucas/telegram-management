import pytest
import os

from dotenv import load_dotenv

from core.plataforms.edduz import Eduzz

load_dotenv(".env", encoding='utf-8')

edduz_email = os.getenv('edduz_email')
api_key = os.getenv('edduz_public_key')
publick_key = os.getenv('edduz_api_key')

edduz = Eduzz(edduz_email, api_key, publick_key)


class TestEduzz:

    def test_get_token(self):
        assert len(edduz.get_token()) == 346

    @pytest.mark.asyncio 
    async def test_get_sale_list(self):
        result = await edduz.get_sale_list(start_date='2020-12-03', end_date='2022-12-03', page=1)
        assert result['success'] == True

    @pytest.mark.asyncio 
    async def test_status_list(self):
        result = await edduz.status_list()
        assert result['success'] == True
        
    @pytest.mark.asyncio 
    async def test_get_contract_list(self):
        result = await edduz.get_contract_list(start_date='2020-12-03', end_date='2022-12-03', page=1)
        assert result['success'] == True
    
    @pytest.mark.asyncio 
    async def test_get_contract(self):
        result = await edduz.get_contract(contract_id=990804, invoice_id=23877715)
        assert result['success'] == True

    @pytest.mark.asyncio 
    async def test_get_total(self):
        result = await edduz.get_total('2020-12-05', '2022-12-05')
        assert result['success'] == True
        
    @pytest.mark.asyncio 
    async def test_get_balance(self):
        result = await edduz.get_balance()
        assert result['success'] == True

    @pytest.mark.asyncio 
    async def test_content_list(self):
        result = await edduz.content_list()
        assert result['success'] == True

    @pytest.mark.asyncio 
    async def test_get_content(self):
        result = await edduz.get_content(content_id=641675)
        assert result['success'] == True