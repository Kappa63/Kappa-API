from Controllers.DBController import initDB
from flasgger import Swagger
from flask import Flask

from APIs.AuthAPI import authBP
from APIs.NewsAPI import newsBP

app = Flask(__name__)
initDB()

SWAGGER_CONFIG = {
    "swagger": "2.0",
    "info": {
        "title": "K-API",
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
        "url": "https://github.com/Kappa63"
    }
}

swagger = Swagger(app, template=SWAGGER_CONFIG)

app.register_blueprint(newsBP, url_prefix="/api")
app.register_blueprint(authBP, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)