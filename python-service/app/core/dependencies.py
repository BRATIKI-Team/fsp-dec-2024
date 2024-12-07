from fastapi_mail import FastMail, ConnectionConfig
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import MAIL_SERVER, MAIL_PASSWORD, MAIL_USERNAME, MAIL_PORT

def get_db() -> AsyncIOMotorDatabase:
    from motor.motor_asyncio import AsyncIOMotorClient
    from app.core.config import DATABASE_CONNECTION_STRING, DATABASE_NAME

    client = AsyncIOMotorClient(DATABASE_CONNECTION_STRING)
    return client.get_database(DATABASE_NAME)


def get_mail() -> FastMail:
    print(MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER)
    config = ConnectionConfig(
        MAIL_SERVER=MAIL_SERVER,
        MAIL_PORT=MAIL_PORT,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_FROM=MAIL_USERNAME,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False
    )

    return FastMail(config)


def transliterate(text):
    cyrillic_to_latin = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH',
        'Ь': '', 'Ы': 'Y', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ь': '', 'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    return ''.join(cyrillic_to_latin.get(char, char) for char in text)

