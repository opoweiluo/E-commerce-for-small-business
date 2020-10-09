from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'david'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

from website import routes