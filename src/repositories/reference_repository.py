from config import db
from sqlalchemy import text
from entities.reference import Reference


def get_references():
    result = db.session.execute(text("""
        SELECT id, citation_key, type, author, title, year, publication
        FROM bibliographic_references
    """))

    return [
        Reference(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        for row in result.fetchall()
    ]