from Controllers.DBController import initDB
from flasgger import Swagger
from flask import Flask
from config import Config
from APIs.AuthAPI import authBP
from APIs.NewsAPI import newsBP
from APIs.AdminAPI import adminBP


app = Flask(__name__)
initDB()

swagger = Swagger(app, template=Config.SWAGGER_CONFIG)

app.register_blueprint(newsBP, url_prefix="/api")
app.register_blueprint(authBP, url_prefix="/api")
app.register_blueprint(adminBP, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)