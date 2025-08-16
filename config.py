from dotenv import load_dotenv, find_dotenv
import os

envPath = find_dotenv()
load_dotenv(envPath)

class Config:
    ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

    # DEFAULT_KEY = os.environ["DEFAULT_KEY"]
    # DEFAULT_USERNAME = os.environ["DEFAULT_USERNAME"]
    # DEFAULT_PASSWORD = os.environ["DEFAULT_PASSWORD"]

    SQL_DB = os.environ["DB"]
    SQL_USERS_TABLE = os.environ["USERS_TABLE"]

    SWAGGER_TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": os.environ["APP_NAME"],
            "description": "The Kappa API",
            "version": "v2.0",
            "contact": {
                "email": "kareem.qiblawi2@outlook.com"
            }
        },
        "basePath": "/api",
        "schemes": ["http"],
        "externalDocs": {
            "description": "GitHub Repository",
            "url": "https://github.com/Kappa63/Kappa-Api"
        },
        # "securityDefinitions": {
        #     "APIKeyHeader": {
        #         "type": "apiKey",
        #         "name": "X-API-Key",
        #         "in": "header"
        #     }
        # },
        # "security": [
        #     {
        #         "APIKeyHeader": []
        #     }
        # ]
    }

    SWAGGER_CONFIG = {
        "headers": [],
        "specs": [
            {
                "endpoint": "APIDocs",
                "route": "/APIDocs",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True
            }
        ],
        "static_url_path": "/flasgger_static",
        "specs_route": "/",
        "title": os.environ["APP_NAME"]
    }
