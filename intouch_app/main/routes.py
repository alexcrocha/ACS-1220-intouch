from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from intouch_app.models import Contact, Note
from intouch_app.main.forms import ContactForm, NoteForm, DeleteForm

from intouch_app.extensions import db

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def homepage():
    """Show homepage."""
    all_contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", contacts=all_contacts)


@main.route("/create_contact", methods=["GET", "POST"])
@login_required
def create_contact():
    form = ContactForm()

    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            birthday=form.birthday.data,
            image_url = form.image_url.data,
            relationship=form.relationship.data,
            user_id=current_user.id,
        )
        db.session.add(new_contact)
        db.session.commit()

        flash("New contact was created successfully.")
        return redirect(url_for("main.contact_detail", contact_id=new_contact.id))
    return render_template("create_contact.html", form=form)


@main.route("/contact/<contact_id>", methods=["GET", "POST"])
@login_required
def contact_detail(contact_id):
    contact = Contact.query.get(contact_id)
    notes = Note.query.filter_by(contact_id=contact_id).all()

    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = ContactForm(obj=contact)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.address = form.address.data
        contact.birthday = form.birthday.data
        contact.image_url = form.image_url.data
        contact.relationship = form.relationship.data

        db.session.commit()

        flash("Contact was updated successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact_id))

    return render_template(
        "contact_detail.html", contact=contact, notes=notes, form=form
    )


@main.route("/contact/<contact_id>/edit", methods=["GET", "POST"])
@login_required
def edit_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = ContactForm(obj=contact)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.address = form.address.data
        contact.birthday = form.birthday.data
        contact.image_url = form.image_url.data
        contact.relationship = form.relationship.data

        db.session.commit()

        flash("Contact was updated successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact_id))

    return render_template("edit_contact.html", contact=contact, form=form)


@main.route("/contact/<contact_id>/delete", methods=["GET", "POST"])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = DeleteForm(obj=contact)

    if form.validate_on_submit():
        db.session.delete(contact)
        db.session.commit()

        flash("Contact was deleted successfully.")
        return redirect(url_for("main.homepage"))
    return render_template("delete_contact.html", contact=contact, form=form)


@main.route("/contact/<contact_id>/create_note", methods=["GET", "POST"])
@login_required
def create_note(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = NoteForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_note = Note(
            note=form.note.data, created_on=datetime.now(), contact_id=contact.id
        )

        db.session.add(new_note)
        db.session.commit()

        flash("New note was created successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact.id))

    return render_template("create_note.html", contact=contact, form=form)


@main.route("/contact/<contact_id>/note/<note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(contact_id, note_id):
    contact = Contact.query.get(contact_id)
    note = Note.query.get(note_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = NoteForm(obj=note)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        note.note = form.note.data
        note.created_on = datetime.now()

        db.session.add(note)
        db.session.commit()

        flash("Note was updated successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact.id))

    return render_template(
        "edit_note.html", contact=contact, note=note, form=form
    )


@main.route("/contact/<contact_id>/note/<note_id>", methods=["GET", "POST"])
@login_required
def delete_note(contact_id, note_id):
    contact = Contact.query.get(contact_id)
    note = Note.query.get(note_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))
    form = DeleteForm(obj=contact)
    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        flash("Note was deleted successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact.id))
    return render_template("delete_note.html", contact=contact, note=note, form=form)
