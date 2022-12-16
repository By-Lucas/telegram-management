from core.configs import settings
from core.database import engine


# Função para criar as tabelas

async def create_tables() -> None:
    import models.__all_models
    print('Criando as tabelas no banco de dados')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso...')


if __name__ == '__main__':
    import asyncio

    """
    Se estiver dando erro (RuntimeError: Event loop is closed), você utiliza o código abaixo;
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    """
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_tables())
