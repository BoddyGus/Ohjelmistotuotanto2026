class UserInputError(Exception):
    pass

def validate_todo(content):
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
          raise UserInputError("Todo content length must be smaller than 100")

def validate_reference(reference_type, citation_key, author, title, year):
    if not citation_key or not reference_type or not author or not title or not year:
        raise UserInputError("Required fields are missing")

    if not str(year).isdigit() or not 0 < int(year) <= 2026:
        raise UserInputError("Year must be a valid number")

    if len(title) > 100:
        raise UserInputError("Title is too long")