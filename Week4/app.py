# main file to run
import os
from flask import Flask
from extensions import db, bcrypt, cors, limiter
from dotenv import load_dotenv
from user_routes import user_bp
from post_routes import post_bp
from admin import create_first_admin

load_dotenv()
def start_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    # Create tables
    with app.app_context():
        db.create_all()
    # create one admin
    create_first_admin(app)
    
    return app

if __name__ == "__main__":
    app = start_app()
    app.run(debug=True)