from Functions.Decorators import Ratelimiter
from Controllers.DBController import initDB
from flask import Flask, Blueprint
from flasgger import Swagger
from config import Config
from redis import Redis

from APIs.AdminAPI import adminBP
from APIs.AuthAPI import authBP
from APIs.WebAPI import webBP
from APIs.UserAPI import userBP

app = Flask(__name__)

redisClient = Redis(host="0.0.0.0", port=6379)
Ratelimiter.init_app(app)

initDB()

swagger = Swagger(app, template=Config.SWAGGER_TEMPLATE, config=Config.SWAGGER_CONFIG)

baseBP = Blueprint("api", __name__, url_prefix="/api")

baseBP.register_blueprint(authBP, url_prefix="/auth") 
baseBP.register_blueprint(webBP, url_prefix="/web")
baseBP.register_blueprint(userBP, url_prefix="/user")
baseBP.register_blueprint(adminBP, url_prefix="/admin")

app.register_blueprint(baseBP)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)