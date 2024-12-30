import json
import os
import secrets

from dotenv import load_dotenv

from framework.enums import EnvType

# loads .env files
load_dotenv()

app_config = None


class Config:
    __APP_CONFIG_FILE_PATH = 'tests/data/app-configs.json'
    __CORS_ENABLED = 'CORS_ENABLED'

    __HEADERS = 'headers'
    __DEFAULT = 'default'
    __CONTENT_TYPE = 'Content-Type'
    __AUTHORIZATION = 'Authorization'
    __X_AUTHORIZATION = 'X-Authorization'
    __BEARER = 'Bearer'
    __ADMIN = 'admin'
    __USER_AGENT = 'user_agent'
    __IPHONE = 'iphone'
    __PLATFORM = 'platform'
    __APP_VERSION = 'appVersion'
    __APP_CONFIG = 'app_config'

    __SECURITY_CONFIGS = 'SECURITY_CONFIGS'
    __ENCRYPTION_CONFIGS = 'ENCRYPTION_CONFIGS'
    __ENCRYPTION_KEY = 'ENCRYPTION_KEY'
    __ENCRYPTION_NONCE = 'ENCRYPTION_NONCE'
    __CLIENT_ID_KEY = 'CLIENT_ID_KEY'
    __CLIENT_ID_SECRET = 'CLIENT_ID_SECRET'

    __SECRET_KEY = 'SECRET_KEY'
    __AWS_SECRET_NAME = 'AWS_SECRET_NAME'

    # Database Configs
    __DB_HOSTNAME = 'DB_HOSTNAME'
    __DB_PORT = 'DB_PORT'
    __DB_NAME = 'DB_NAME'
    __DB_USERNAME = 'DB_USERNAME'
    __DB_PASSWORD = 'DB_PASSWORD'

    ENCRYPTION_KEY = None
    ENCRYPTION_NONCE = None

    # env configs
    CORS_ENABLED = bool(os.getenv(__CORS_ENABLED))

    if EnvType.is_testing(EnvType.get_env_type()):
        # loads app's config file
        with open(__APP_CONFIG_FILE_PATH) as config_file:
            APP_CONFIGS = json.load(config_file)

        SECURITY_CONFIGS = APP_CONFIGS.get(__SECURITY_CONFIGS)

        # Database Configs
        DB_HOSTNAME = os.getenv(__DB_HOSTNAME)
        DB_PORT = os.getenv(__DB_PORT)
        DB_NAME = "".join(["test", os.getenv(__DB_NAME).title()])
        DB_USERNAME = os.getenv(__DB_USERNAME)
        DB_PASSWORD = os.getenv(__DB_PASSWORD)
    else:
        SEED = secrets.token_hex(16)

        # security configs
        SECURITY_CONFIGS = os.getenv(__SECURITY_CONFIGS)
        AWS_SECRET_NAME = os.getenv(__AWS_SECRET_NAME)
        SECRET_KEY = os.getenv(__SECRET_KEY)

        # Database Configs
        DB_HOSTNAME = os.getenv(__DB_HOSTNAME)
        DB_PORT = os.getenv(__DB_PORT)
        DB_NAME = os.getenv(__DB_NAME)
        DB_USERNAME = os.getenv(__DB_USERNAME)
        DB_PASSWORD = os.getenv(__DB_PASSWORD)

    if SECURITY_CONFIGS:
        ENCRYPTION_CONFIGS = SECURITY_CONFIGS.get(__ENCRYPTION_CONFIGS)
        ENCRYPTION_KEY = ENCRYPTION_CONFIGS.get(__ENCRYPTION_KEY)
        ENCRYPTION_NONCE = ENCRYPTION_CONFIGS.get(__ENCRYPTION_NONCE)

    @staticmethod
    def is_cors_enabled():
        return Config.CORS_ENABLED
