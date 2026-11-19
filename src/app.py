from flask import render_template, jsonify, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from db_helper import reset_db
from repositories.reference_repository import get_references, add_reference
from reference_validation import (
    ReferenceValidationError,
    is_duplicate_citation_key,
    validate_reference,
)
from reference_types import get_reference_type
from config import app, db, test_env


@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)


@app.route("/new_reference", methods=["GET", "POST"])
def new_reference():
    if request.method == "GET":
        return render_template("add_reference.html", form_data={})

    form_data = request.form
    try:
        reference_data = validate_reference(form_data)
    except ReferenceValidationError as error:
        flash(str(error))
        return render_template("add_reference.html", form_data=form_data), 400

    if get_reference_type(reference_data["reference_type"]) is None:
        flash("Unsupported reference type. Choose book, article, or inproceedings.")
        return render_template("add_reference.html", form_data=form_data), 400

    try:
        add_reference(**reference_data)
    except IntegrityError as error:
        db.session.rollback()
        if is_duplicate_citation_key(error):
            flash("The citation key is already in use.")
        else:
            flash(
                "Could not add reference because one or more values are invalid. "
                "Check the citation key and reference details."
            )
        return render_template("add_reference.html", form_data=form_data), 400
    flash("Reference added successfully.", "success")
    return redirect(url_for("index"))


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
