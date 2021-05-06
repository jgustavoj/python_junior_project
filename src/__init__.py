from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'book.sqlite'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sws/2edc??//bkomk00\\dff34c//dcvg//[[sf526\\`sk~ep;x^^df\\dfxc'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import User, Todo

    create_database(app)

    #Authorization 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return app 

def create_database(app):
    if not path.exists('src/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

