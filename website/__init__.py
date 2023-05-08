from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from local.env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'local.env')
load_dotenv(dotenv_path=dotenv_path)

# connect to postgres database using local.env
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

db = SQLAlchemy()
db_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'simple-web-based-visualization-application'
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
