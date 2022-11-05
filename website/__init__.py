#import flask - from the package import class
from flask import Flask, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db=SQLAlchemy()

def create_app():
  
    app=Flask(__name__) 
    app.debug=True
    app.secret_key='utroutoru'
    
    # allow postgres and sqlite compatability
    # get DATABASE_URL from environment variables (heroku)
    if "DATABASE_URL" in os.environ:
        uri = os.environ['DATABASE_URL']
        if uri and uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
    else:
        uri = "sqlite:///IAB207_MUSICEVENTS_DB.db"

    # set db uri
    app.config['SQLALCHEMY_DATABASE_URI']=uri

    # Initialise DB with flask
    db.init_app(app)

    bootstrap = Bootstrap5(app)

    login_manager = LoginManager()

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect('/404', code=302)
    
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    # create user loader function that takes userid and returns User
    from .models import User  
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    # import the different views
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import events
    app.register_blueprint(events.bp)
    
    return app



