from flask import Flask 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sws/2edc??//bkomk00\\dff34c//dcvg//[[sf526\\`sk~ep;x^^df\\dfxc'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app 