from Functions.Decorators import Ratelimiter
from Controllers.DBController import initDB
from flask import Flask
from flasgger import Swagger
from config import Config
from redis import Redis

from APIs.AdminAPI import adminBP
from APIs.AuthAPI import authBP
from APIs.NewsAPI import newsBP

app = Flask(__name__)
redisClient = Redis(host="0.0.0.0", port=6379)
Ratelimiter.init_app(app)
initDB()

swagger = Swagger(app, template=Config.SWAGGER_CONFIG)

app.register_blueprint(newsBP, url_prefix="/api")
app.register_blueprint(authBP, url_prefix="/api")
app.register_blueprint(adminBP, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)