import os
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from website.forms import RecipeForm, SearchForm
from website.models import db, Recipe, Favorite
from werkzeug.utils import secure_filename

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    favorites = Favorite.query.all()
    return render_template('home.html', favorites=favorites)

@routes.route('/add-to-favorites/<int:recipe_id>', methods=['POST'])
def add_to_favorites(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    # Check if the recipe is already in the favorites
    existing_favorite = Favorite.query.filter_by(recipe_id=recipe_id).first()
    if existing_favorite:
        flash(f'Recipe {recipe.name} is already in your favorites!', 'danger')
    else:
        new_favorite = Favorite(recipe_id=recipe.id)
        db.session.add(new_favorite)
        db.session.commit()
        flash(f'Recipe {recipe.name} added to favorites!', 'success')
    return redirect(url_for('routes.home', id=recipe_id))

@routes.route('/remove-from-favorites/<int:recipe_id>', methods=['POST'])
def remove_from_favorites(recipe_id):
    favorite = Favorite.query.filter_by(recipe_id=recipe_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('Recipe removed from favorites!', 'success')
    else:
        flash('Recipe not found in favorites!', 'danger')
    return redirect(url_for('routes.home'))


@routes.route('/create-recipe', methods=['GET', 'POST'])
def create_recipe():
    name = None
    form = RecipeForm()
    if form.validate_on_submit():
        name = Recipe.query.filter_by(name=form.name.data).first()
        if name is None:
            # Handle file upload
            image_url = None
            if form.image.data:
                file = form.image.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_url = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            
            recipe = Recipe(
                name=form.name.data, 
                category=form.category.data, 
                ingredients=form.ingredients.data, 
                instructions=form.instructions.data,
                image=image_url
            )
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
    favorite_recipes = Favorite.query.all() 
    return render_template('admin.html', our_recipes=our_recipes, favorite_recipes=favorite_recipes)


@routes.route('/salads')
def salads():
    salads = Recipe.query.filter_by(category='salads').all()
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

@routes.route('/delete-recipe/<int:id>')
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    name = None
    form = RecipeForm()
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        flash(f'Recipe deleted for {recipe_to_delete.name}!', 'success')
        return redirect(url_for('routes.create_recipe', name=name, form=form))
    except:
        flash('There was an issue deleting your recipe.', 'danger')
    return render_template('add-recipe.html', form=form, name=name)

@routes.route('/recipe/<int:id>')
def recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

@routes.route('/update-recipe/<int:id>', methods=['GET', 'POST'])
def update_recipe(id):
    recipe_to_update = Recipe.query.get_or_404(id)
    form = RecipeForm(obj=recipe_to_update)

    if form.validate_on_submit():
        recipe_to_update.name = form.name.data
        recipe_to_update.category = form.category.data
        recipe_to_update.ingredients = form.ingredients.data
        recipe_to_update.instructions = form.instructions.data
        
        if 'image' in request.files:  # Check if 'image' file is in the form data
            file = request.files['image']  # Access the uploaded file
            if file.filename != '':  # Check if a file was selected
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                recipe_to_update.image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

        try:
            db.session.commit()
            flash(f'Recipe updated for {recipe_to_update.name}!', 'success')
            return redirect(url_for('routes.recipe', id=id))
        except:
            flash('There was an issue updating your recipe.', 'danger')
    return render_template('update.html', form=form, recipe_to_update=recipe_to_update, id=id)


# Pass the Search form to the to Navbar
@routes.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Search for recipes by name
@routes.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.searched.data
        # Filter and order the results before converting to a list
        recipes = Recipe.query.filter(Recipe.name.contains(searched)).order_by(Recipe.name).all()
        return render_template('search.html', form=form, searched=searched, recipes=recipes)
    return render_template('search.html', form=form, recipes=[])
