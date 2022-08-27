import os

from typing import Optional, Union

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(
    name, silent: bool = False, default: Optional[Union[str, int]] = None
) -> Optional[Union[str, int]]:
    """
    Retrieves variable value from both os env and .env files
    :param name: variable name
    :param silent: if False, error will be raised when variable is not set or is empty string
    :param default: default value to use if env var is absent
    :return: variable value
    """
    try:
        var = os.environ[name]
        assert var is not None and var != ""
        return str(os.environ[name])
    except (KeyError, AssertionError):
        if default is not None:
            return default
        if silent:
            return None
        message = f"Expected environment variable '{name}' not set."
        raise OSError(message)


LOCALHOST = get_env_variable('LOCALHOST')
LOCALHOST_PORT = get_env_variable('LOCALHOST_PORT')

POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

TEST_POSTGRES_URL = get_env_variable("TEST_POSTGRES_URL")
TEST_POSTGRES_USER = get_env_variable("TEST_POSTGRES_USER")
TEST_POSTGRES_PW = get_env_variable("TEST_POSTGRES_PW")
TEST_POSTGRES_DB = get_env_variable("TEST_POSTGRES_DB")

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"
TEST_DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"

DEV = get_env_variable("FLASK_ENV") == "development"
DEBUG = True
FLASK_APP = get_env_variable('FLASK_APP')

FLASK_TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": DB_URL,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "OPENAPI_VERSION": "3.0.3",
    "OPENAPI_URL_PREFIX": "/",
    "OPENAPI_SWAGGER_UI_PATH": "/test-api-docs",
    "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    "SQLALCHEMY_ECHO": False,
    "API_TITLE": "TEST PARKING API",
    "API_VERSION": "v1",
    "CORS_METHODS": ["GET", "OPTIONS", "POST", "HEAD", "PUT", "DELETE"],
    "CORS_SEND_WILDCARD": False,
    "CORS_SUPPORTS_CREDENTIALS": True,
    "CORS_ALLOW_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
        "content-type",
        "x-proxysession-id",
    ],
    "CORS_EXPOSE_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
    ],
    "CORS_ORIGINS": [
        r"^.*192.168.*$",
        r"^.*localhost.*$",
    ],
    "CORS_AUTOMATIC_OPTIONS": True,
}

FLASK_DEV_CONFIG = {
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SQLALCHEMY_DATABASE_URI": DB_URL,
    "OPENAPI_VERSION": "3.0.3",
    "OPENAPI_URL_PREFIX": "/",
    "OPENAPI_SWAGGER_UI_PATH": "/api-docs",
    "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    "SQLALCHEMY_ECHO": True,
    "API_TITLE": "PARKING API",
    "API_VERSION": "v1",
    "CORS_METHODS": ["GET", "OPTIONS", "POST", "HEAD", "PUT", "DELETE"],
    "CORS_SEND_WILDCARD": False,
    "CORS_SUPPORTS_CREDENTIALS": True,
    "CORS_ALLOW_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
        "content-type",
        "x-proxysession-id",
    ],
    "CORS_EXPOSE_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
    ],
    "CORS_ORIGINS": [
        r"^.*192.168.*$",
        r"^.*localhost.*$",
        r"^.*seller-online.*$",
    ],
    "CORS_AUTOMATIC_OPTIONS": True,
}

FLASK_PROD_CONFIG = {}

# APSCHEDULER_RUN_INTERVAL = {"minutes": 1 if DEBUG else 10}

PROCRASTINATE_SCRIPT_PATH = f"{os.getcwd()}/scripts/run_jobs_worker"

CACHING_OPTIONS = {
    "DEBUG": DEBUG,
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 60,
    "CACHE_KEY_PREFIX": "som_",
    "CACHE_REDIS_HOST": get_env_variable(
        "REDIS_HOST", silent=True, default="localhost"
    ),
    "CACHE_REDIS_PORT": get_env_variable("REDIS_HOST", silent=True, default=6379),
    # "CACHE_REDIS_PASSWORD": "",
    "CACHE_REDIS_DB": 3,
    # "CACHE_REDIS_URL": "",
}


SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 20, "max_overflow": 0}


HARDCODED_PARKING_ID = 534013
DEFAULT_REFRESH_PERIOD = 1
PARKING_EXTERNAL_API_ENDPOINT = (
    "http://private-b2c96-mojeprahaapi.apiary-mock.com/pr-parkings/"
)
