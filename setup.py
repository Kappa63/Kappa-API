from Functions.Decorators import Ratelimiter
from Controllers.DBController import initDB
from flask import Flask, Blueprint
from flasgger import Swagger
from flask_cors import CORS
from Config import EnvConfig, APIConfig, MPortfolioConfig
from redis import Redis
import os

from APIs.PortfolioAPI import portfolioBP
from APIs.AdminAPI import adminBP
from APIs.AuthAPI import authBP
from APIs.WebAPI import webBP
from APIs.UserAPI import userBP

app = Flask(__name__)
CORS(app, origins=["http://localhost:63342", "http://127.0.0.1:3000"])

redisClient = Redis(host="0.0.0.0", port=6379)
Ratelimiter.init_app(app)

initDB()

swagger = Swagger(app, template=APIConfig.SWAGGER_TEMPLATE(EnvConfig.APP_NAME), config=APIConfig.SWAGGER_CONFIG(EnvConfig.APP_NAME))

os.makedirs(MPortfolioConfig.PORTFOLIO_UPLOADS_FOLDER, exist_ok=True)

baseBP = Blueprint("api", __name__, url_prefix="/api")

baseBP.register_blueprint(authBP, url_prefix="/auth") 
baseBP.register_blueprint(webBP, url_prefix="/web")
baseBP.register_blueprint(userBP, url_prefix="/user")
baseBP.register_blueprint(adminBP, url_prefix="/admin")
baseBP.register_blueprint(portfolioBP, url_prefix="/portfolio")

app.register_blueprint(baseBP)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)