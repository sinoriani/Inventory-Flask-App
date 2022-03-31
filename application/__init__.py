from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect
from application.config import Config
from application.users.models import get_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from application.languages import LANG
from application.database import DATABASE_NAME

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
csrf = None

@login_manager.user_loader
def user_loader(user_id):
    return get_user(id=user_id)



from datetime import date

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf = CsrfProtect(app)
    bcrypt.init_app(app)

    from application.users.routes import users 
    from application.errors.handlers import errors
    from application.main.routes import main 
    from application.inventory.routes import inventory 
    from application.tasks.routes import tasks 
    from application.affairs.routes import affairs 
    app.register_blueprint(affairs)
    app.register_blueprint(tasks)
    app.register_blueprint(inventory)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.jinja_env.globals['LANG'] = LANG
    app.jinja_env.globals['dbname'] = DATABASE_NAME

    return app


