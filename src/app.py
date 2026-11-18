from flask import render_template, jsonify
from db_helper import reset_db
from repositories.reference_repository import get_references
from config import app, test_env


@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)


@app.route("/new_reference")
def new_reference():
    return render_template("add_reference.html")


if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
