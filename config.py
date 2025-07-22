from dotenv import load_dotenv, find_dotenv
import os

envPath = find_dotenv()
load_dotenv(envPath)

class Config:
    ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

    SQL_DB = os.environ["DB"]
    SQL_USERS_TABLE = os.environ["USERS_TABLE"]

    SWAGGER_CONFIG = {
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
        }
    }
