def format_reference(entry_type, reference, publication_field):
    fields = [
        ("author", reference.author),
        ("title", reference.title),
        ("year", reference.year),
    ]
    
    publication = (reference.publication or "").strip()
    if publication:
        fields.append((publication_field, publication))

    formatted_fields = ",\n".join(
        f" {name} = {{{value}}}" for name, value in fields
    )
    return f"@{entry_type}{{{reference.citation_key},\n{formatted_fields}\n}}"

def format_inproceeding_reference(reference):
    return format_reference("inproceedings", reference, "booktitle")

def format_article_reference(reference):
    return format_reference("article", reference, "journal")

def format_book_reference(reference):
    return format_reference("book", reference, "publisher")