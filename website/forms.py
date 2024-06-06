from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class RecipeForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    category_choices = [
        ('salads', 'Salads'),
        ('meat', 'Meat'),
        ('dairy', 'Dairy'),
        ('dessert', 'Dessert')
    ]
    # Use SelectField for category with predefined choices
    category = SelectField('Category:', choices=category_choices, validators=[DataRequired()])
    ingredients = CKEditorField('Ingredients:', validators=[DataRequired()])
    instructions = CKEditorField('Instructions:', validators=[DataRequired()])
    image = FileField('Image:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    searched = StringField('Search:', validators=[DataRequired()])
    submit = SubmitField('Submit')
