from flask import Flask
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from website.controller import routes
from website.module import db
import os

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes)
    CKEditor(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0" ,debug=True)