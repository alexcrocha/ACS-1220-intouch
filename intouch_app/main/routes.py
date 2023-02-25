from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from intouch_app.models import Contact, Comment, User
from intouch_app.main.forms import ContactForm

from intouch_app.extensions import db

main = Blueprint('main', __name__)

# Create your routes here.

@main.route('/')
@login_required
def homepage():
    """Show homepage."""
    return render_template('home.html')

@main.route('/create_contact', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = ContactForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_contact = Contact(
            name = form.name.data,
            email = form.email.data,
            phone = form.phone.data,
            address = form.address.data,
            birthday = form.birthday.data,
            user_id = current_user.id
        )
        db.session.add(new_contact)
        db.session.commit()

        flash('New contact was created successfully.')
        return redirect(url_for('main.contact_detail', contact_id=new_contact.id))
    return render_template('create_contact.html', form=form)
