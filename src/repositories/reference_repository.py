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


def add_reference(citation_key, reference_type, author, title, year, publication):
    db.session.execute(
        text("""
            INSERT INTO bibliographic_references
                (citation_key, type, author, title, year, publication)
            VALUES
                (:citation_key, :type, :author, :title, :year, :publication)
        """),
        {
            "citation_key": citation_key,
            "type": reference_type,
            "author": author,
            "title": title,
            "year": year,
            "publication": publication,
        },
    )
    db.session.commit()

def get_reference(reference_id):
    result = db.session.execute(
        text("""
            SELECT id, citation_key, type, author, title, year, publication
            FROM bibliographic_references
            WHERE id = :id
        """),
        {"id": reference_id},
    )
    row = result.fetchone()

    if row is None:
        return None

    return Reference(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

def delete_reference(reference_id):
    result = db.session.execute(
        text("""
            DELETE FROM bibliographic_references
            WHERE id = :id
        """),
        {"id": reference_id},
    )
    db.session.commit()
    return result.rowcount > 0
