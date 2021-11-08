from wtforms import StringField,TextAreaField, SubmitField, SelectField 
from wtforms.validators import Required, Email, Length
from flask_wtf import FlaskForm

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell Us About Yourself...',validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    bio = TextAreaField('About...', validators=[Required(), Length(1, 100)])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post_title = StringField('Pitch title', validators=[Required()])
    post_category = SelectField('Pitch category',choices=[('Select a category','Select a category'),('Pickup lines', 'Pickup lines'),('Interview','Interview'),('Product','Product'),('Promotions','Promotions')], validators=[Required()])
    post_content = StringField('What is in your mind?')
    submit = SubmitField('Submit')
    
# class CategoryForm(FlaskForm):
#     name = StringField('Category Name', validators=[Required(), Length(1, 64)])
#     submit = SubmitField('Submit')


# class CommentForm(FlaskForm):
#     body = TextAreaField('Comment', validators=[Required()])
#     submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Body', validators=[Required()])
    submit = SubmitField('Submit')