from intouch_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class Contact(db.Model):
    """Contact model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    birthday = db.Column(db.Date)
    image_url = db.Column(db.String(400))
    relationship = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __str__(self):
        return f"<Contact: {self.name}>"

    def __repr__(self):
        return f"<Contact: {self.name}>"


class Note(db.Model):
    """Contact model."""

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(800), nullable=False)
    created_on = db.Column(db.Date)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)

    def __str__(self):
        return f"<Contact: {self.name}>"

    def __repr__(self):
        return f"<Contact: {self.name}>"


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"
