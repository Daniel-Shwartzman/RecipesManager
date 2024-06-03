from flask import Blueprint, render_template, flash, request
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
    return render_template('add-recipe.html', form=form, name=name)

@routes.route('/admin')
def admin():
    our_recipes = Recipe.query.order_by(Recipe.date_created).all()
    return render_template('admin.html', our_recipes=our_recipes)

@routes.route('/salads')
def salads():
    salads = Recipe.query.filter_by(category='salad').all()
    return render_template('salads.html', salads=salads)

@routes.route('/meat')
def meat():
    meat = Recipe.query.filter_by(category='meat').all()
    return render_template('meat.html', meat=meat)

@routes.route('/dairy')
def dairy():
    dairy = Recipe.query.filter_by(category='dairy').all()
    return render_template('dairy.html', dairy=dairy)

@routes.route('/desserts')
def desserts():
    desserts = Recipe.query.filter_by(category='dessert').all()
    return render_template('desserts.html', desserts=desserts)

@routes.route('/update-recipe/<int:id>', methods=['GET', 'POST'])
def update_recipe(id):
    recipe_to_update = Recipe.query.get_or_404(id)
    form = RecipeForm(obj=recipe_to_update)

    if form.validate_on_submit():
        recipe_to_update.name = form.name.data
        recipe_to_update.category = form.category.data
        recipe_to_update.ingredients = form.ingredients.data
        recipe_to_update.instructions = form.instructions.data
        try:
            db.session.commit()
            flash(f'Recipe updated for {recipe_to_update.name}!', 'success')
            return render_template('update.html', form=form, recipe_to_update=recipe_to_update)
        except:
            flash('There was an issue updating your recipe.', 'danger')
    return render_template('update.html', form=form, recipe_to_update=recipe_to_update, id=id)

@routes.route('/delete-recipe/<int:id>')
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    name = None
    form = RecipeForm()
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        flash(f'Recipe deleted for {recipe_to_delete.name}!', 'success')
        return render_template('recipe.html', form=form, name=name)
    except:
        flash('There was an issue deleting your recipe.', 'danger')
    return render_template('recipe.html', form=form, name=name)

@routes.route('/recipes/<int:id>')
def recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)