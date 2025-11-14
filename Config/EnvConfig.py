from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

SQL_DB = os.environ["DB"]
SQL_USERS_TABLE = os.environ["USERS_TABLE"]

APP_NAME = os.environ["APP_NAME"]