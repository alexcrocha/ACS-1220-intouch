# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    """Form to create a contact."""
    name = StringField('Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email')
    phone = StringField('Phone')
    address = StringField('Address')
    birthday = DateField('Birthday')
    relationship = StringField('Relationship')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """Form to create a contact."""
    comment = TextAreaField('Name',
        validators=[DataRequired(), Length(min=3, max=500)])
    submit = SubmitField('Submit')
