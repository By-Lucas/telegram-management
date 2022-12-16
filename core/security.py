from passlib.context import CryptContext
# passlib se desejar, é bom saber mais sobre a biblioteca utilizada


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(password: str, hash_password: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando
    a senha em texto puro, informada pelo usuário, e o hash da senha
    que estará salvo no banco de dados durante a criação
    da conta.
    """
    return CRIPTO.verify(password, hash_password)


def gerar_hash_senha(password: str) -> str:
    """
    Função que gera e retona o hash da senha
    """
    return CRIPTO.hash(password)