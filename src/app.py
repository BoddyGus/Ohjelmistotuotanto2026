from flask import render_template, jsonify, request, flash, redirect, url_for
from db_helper import reset_db
from repositories.reference_repository import get_references, add_reference
from reference_validation import ReferenceValidationError, validate_reference
from config import app, test_env


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

    add_reference(**reference_data)
    return redirect(url_for("index"))


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
