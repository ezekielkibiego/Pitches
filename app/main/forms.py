from wtforms import StringField,TextAreaField, SubmitField, SelectField
from wtforms.validators import Required
from flask_wtf import FlaskForm

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell Us About Yourself...',validators = [Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post_title = StringField('Pitch title', validators=[Required()])
    # pitch_category = SelectField('Pitch category',choices=[('Select a category','Select a category'),('Pickup lines', 'Pickup lines'),('Interview','Interview'),('Product','Product'),('Promotions','Promotions')], validators=[Required()])
    comment = StringField('What is in your mind?')
    submit = SubmitField('Submit')
    