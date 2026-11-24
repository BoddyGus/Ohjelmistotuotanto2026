from flask import render_template, jsonify, request, flash, redirect, url_for, Response, abort
from sqlalchemy.exc import IntegrityError
from db_helper import reset_db
from repositories.reference_repository import get_references, add_reference, get_reference
from reference_validation import (
    ReferenceValidationError,
    is_duplicate_citation_key,
    validate_reference,
)
from reference_types import get_reference_type
from config import app, db, test_env
from repositories.bibtex_formatter import (
    format_inproceeding_reference,
    format_article_reference,
    format_book_reference,
)


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

@app.route("/references/<int:reference_id>")
def reference_details(reference_id):
    reference = get_reference(reference_id)

    if reference is None:
        return render_template("reference_not_found.html"), 404

    return render_template("reference_details.html", reference=reference)

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })

@app.route("/export/bibtex")
def export_bibtex():
    formatters = {
        "inproceedings": format_inproceeding_reference,
        "article": format_article_reference,
        "book": format_book_reference,
    }

    entries = []
    for reference in get_references():
        formatter = formatters.get(reference.type)
        if formatter is None:
            abort(500, description=f"Unsupported reference type: {reference.type}")
        entries.append(formatter(reference))

    return Response(
        "\n\n".join(entries),
        mimetype="application/x-bibtex",
        headers={"Content-Disposition": 'attachment; filename="references.bib"'},
    )
