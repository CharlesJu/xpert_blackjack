from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

SESSION_TYPE = 'redis'
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models