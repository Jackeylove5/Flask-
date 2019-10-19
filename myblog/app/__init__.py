# 生成app
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

# 创建一个生成app的函数
def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    # 注册蓝图
    # 注册处理错误的蓝图对象
    from app.errors import bp
    app.register_blueprint(bp)
    from app.auth import bp
    app.register_blueprint(bp)
    from app.main import bp
    app.register_blueprint(bp)

    return app
from app import models


