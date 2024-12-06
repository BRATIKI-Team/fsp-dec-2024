from starlette.config import Config

config = Config(".env")

APP_HOST = config("APP_HOST", cast=str)
APP_NAME = config("APP_NAME", cast=str)

CLIENT_HOST = config("CLIENT_HOST", cast=str)

DATABASE_CONNECTION_STRING = config("DATABASE_CONNECTION_STRING", cast=str)
DATABASE_NAME = config("DATABASE_NAME", cast=str)

JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=str)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str)

RESET_PASSWORD_TOKEN_EXPIRE_MINUTES = config("RESET_PASSWORD_TOKEN_EXPIRE_MINUTES", cast=int)
RESET_PASSWORD_TOKEN_URL = config("RESET_PASSWORD_TOKEN_URL", cast=str)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
