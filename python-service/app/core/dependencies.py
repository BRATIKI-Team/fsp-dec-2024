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
