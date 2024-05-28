from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

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
    ingredients = TextAreaField('Ingredients:', validators=[DataRequired()])
    instructions = TextAreaField('Instructions:', validators=[DataRequired()])
    submit = SubmitField('Submit')
