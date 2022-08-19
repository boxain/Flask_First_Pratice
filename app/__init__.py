from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
from .database import db # .是以下所有都可匯入
from .config import configs # import 字典
from flaskext.markdown import Markdown
from .user_helper import login_manager


mail = Mail()
pagedown = PageDown()


def create_app(env):
    # 初始化flask
    app = Flask(__name__,template_folder="../templates",static_folder="../static")
    
    # 修改flask設定
    app.config.from_object(configs[env])

    # 串接flask各class
    login_manager.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    Markdown(app)

    # Blueprint
    from .main import main_bp

    app.register_blueprint(main_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    return app