from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceType:
    name: str
    label: str
    publication_label: str
    bibtex_field: str


REFERENCE_TYPES = {
    "book": ReferenceType(
        name="book",
        label="Book",
        publication_label="Publisher",
        bibtex_field="publisher",
    ),
    "article": ReferenceType(
        name="article",
        label="Article",
        publication_label="Journal",
        bibtex_field="journal",
    ),
    "inproceedings": ReferenceType(
        name="inproceedings",
        label="Conference paper",
        publication_label="Conference / proceedings title",
        bibtex_field="booktitle",
    ),
}

def get_reference_types():
    """Return all supported reference types (e.g. for a form dropdown)."""
    return list(REFERENCE_TYPES.values())


def get_reference_type(name):
    """Return the reference type with the given name, or None if unsupported."""
    return REFERENCE_TYPES.get(name)