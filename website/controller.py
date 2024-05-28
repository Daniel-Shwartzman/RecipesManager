from flask import Blueprint, render_template, flash
from website.forms import RecipeForm
from website.module import db, Recipe

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/create-recipe', methods=['GET', 'POST'])
def create_recipe():
    name = None
    form = RecipeForm()
    if form.validate_on_submit():
        name = Recipe.query.filter_by(name=form.name.data).first()
        if name is None:
            recipe = Recipe(name=form.name.data, category=form.category.data, ingredients=form.ingredients.data, instructions=form.instructions.data)
            db.session.add(recipe)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.category.data = ''
        form.ingredients.data = ''
        form.instructions.data = ''
        flash(f'Recipe created for {name}!', 'success')
    return render_template('recipe.html', form=form, name=name)

@routes.route('/admin')
def admin():
    our_recipes = Recipe.query.order_by(Recipe.date_created).all()
    return render_template('admin.html', our_recipes=our_recipes)

@routes.route('/salads')
def salads():
    our_recipes = Recipe.query.order_by(Recipe.date_created).all()
    return render_template('salads.html', our_recipes=our_recipes)

@routes.route('/meat')
def meat():
    our_recipes = Recipe.query.order_by(Recipe.date_created).all()
    return render_template('meat.html', our_recipes=our_recipes)

@routes.route('/dairy')
def dairy():
    our_recipes = Recipe.query.order_by(Recipe.date_created).all()
    return render_template('dairy.html', our_recipes=our_recipes)

@routes.route('/desserts')
def desserts():
    our_recipes = Recipe.query.order_by(Recipe.date_created).all()
    return render_template('desserts.html', our_recipes=our_recipes)