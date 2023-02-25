# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    """Form to create a contact."""
    name = StringField('Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email')
    phone = StringField('Phone')
    address = StringField('Address')
    birthday = DateField('Birthday')
    submit = SubmitField('Submit')
