from flask import Flask
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from website.routes import routes
from website.models import db
import os

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='website/templates', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['UPLOAD_FOLDER'] = 'static/images'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes)
    CKEditor(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000 ,debug=True)