from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from intouch_app.models import Contact, Comment
from intouch_app.main.forms import ContactForm, CommentForm

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

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            birthday=form.birthday.data,
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
    comments = Comment.query.filter_by(contact_id=contact_id).all()

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
        contact.relationship = form.relationship.data

        db.session.commit()

        flash("Contact was updated successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact_id))

    return render_template(
        "contact_detail.html", contact=contact, comments=comments, form=form
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
        contact.relationship = form.relationship.data

        db.session.commit()

        flash("Contact was updated successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact_id))

    return render_template("edit_contact.html", contact=contact, form=form)


@main.route("/contact/<contact_id>/delete", methods=["POST"])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    db.session.delete(contact)
    db.session.commit()

    flash("Contact was deleted successfully.")
    return redirect(url_for("main.homepage"))


@main.route("/contact/<contact_id>/create_comment", methods=["GET", "POST"])
@login_required
def create_comment(contact_id):
    contact = Contact.query.get(contact_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = CommentForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_comment = Comment(
            comment=form.comment.data, created_on=datetime.now(), contact_id=contact.id
        )

        db.session.add(new_comment)
        db.session.commit()

        flash("New comment was created successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact.id))

    return render_template("create_comment.html", contact=contact, form=form)


@main.route("/contact/<contact_id>/comment/<comment_id>/edit", methods=["GET", "POST"])
@login_required
def edit_comment(contact_id, comment_id):
    contact = Contact.query.get(contact_id)
    comment = Comment.query.get(comment_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    form = CommentForm(obj=comment)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.created_on = datetime.now()

        db.session.add(comment)
        db.session.commit()

        flash("Comment was updated successfully.")
        return redirect(url_for("main.contact_detail", contact_id=contact.id))

    return render_template(
        "edit_comment.html", contact=contact, comment=comment, form=form
    )


@main.route("/contact/<contact_id>/comment/<comment_id>", methods=["POST"])
@login_required
def delete_comment(contact_id, comment_id):
    contact = Contact.query.get(contact_id)
    comment = Comment.query.get(comment_id)
    if contact is None or contact.user_id != current_user.id:
        return redirect(url_for("main.homepage"))

    db.session.delete(comment)
    db.session.commit()

    flash("Comment was deleted successfully.")
    return redirect(url_for("main.contact_detail", contact_id=contact.id))
