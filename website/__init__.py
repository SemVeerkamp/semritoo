from flask import Flask 

from .commands import create_tables

from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    

    app.config.from_pyfile(config_file)

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Prediction

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    app.cli.add_command(create_tables)

    return app
    
