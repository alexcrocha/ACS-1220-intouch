from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    """Form to create a contact."""

    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email")
    phone = StringField("Phone")
    address = StringField("Address")
    birthday = DateField("Birthday")
    image_url = StringField("Image URL")
    relationship = StringField("Relationship")
    submit = SubmitField("Save")


class NoteForm(FlaskForm):
    """Form to create a note."""

    note = TextAreaField(
        "Note", validators=[DataRequired(), Length(min=3, max=800)]
    )
    submit = SubmitField("Save")

class DeleteForm(FlaskForm):
    """Form to delete a contact or note."""

    submit = SubmitField("Delete")
