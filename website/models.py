from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(10), nullable=False)
    ingredients = db.Column(db.String(5000), nullable=False)
    instructions = db.Column(db.String(10000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Recipe {self.name}>'
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('favorites', lazy=True))

    def __repr__(self):
        return f'<Favorite {self.recipe.name}>'
