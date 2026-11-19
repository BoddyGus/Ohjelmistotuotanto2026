class ReferenceValidationError(Exception):
    """Raised when submitted reference data is invalid."""


def is_duplicate_citation_key(error):
    """Return whether a database integrity error is a citation-key conflict."""
    original_error = error.orig
    if "UNIQUE constraint failed: bibliographic_references.citation_key" in str(original_error):
        return True

    diagnostic = getattr(original_error, "diag", None)
    return getattr(diagnostic, "constraint_name", None) == "bibliographic_references_citation_key_key"


REQUIRED_REFERENCE_FIELDS = {
    "citation_key": "Citation key",
    "type": "Type",
    "author": "Author",
    "title": "Title",
    "year": "Year",
}


def validate_reference(form_data):
    """Validate and normalize reference form data for persistence."""
    missing_fields = [
        label
        for field, label in REQUIRED_REFERENCE_FIELDS.items()
        if not form_data.get(field, "").strip()
    ]
    if missing_fields:
        raise ReferenceValidationError(
            "Please fill in the required fields: " + ", ".join(missing_fields) + "."
        )

    try:
        year = int(form_data["year"])
    except (TypeError, ValueError) as error:
        raise ReferenceValidationError("Year must be a number.") from error

    return {
        "citation_key": form_data["citation_key"].strip(),
        "reference_type": form_data["type"].strip(),
        "author": form_data["author"].strip(),
        "title": form_data["title"].strip(),
        "year": year,
        "publication": form_data.get("publication", "").strip() or None,
    }
