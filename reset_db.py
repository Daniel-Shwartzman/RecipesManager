from website.module import db
from app import create_app

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    # Create all tables
    db.create_all()
    print("Database has been reset.")
