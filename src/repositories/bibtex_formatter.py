def format_inproceeding_reference(reference):
    return (
        f"@inproceedings{{{reference.citation_key},\n"
        f"  author = {{{reference.author}}},\n"
        f"  title = {{{reference.title}}},\n"
        f"  year = {{{reference.year}}},\n"
        f"  booktitle = {{{reference.publication or ''}}}\n"
        "}"
    )

def format_article_reference(reference):
    return (
        f"@article{{{reference.citation_key},\n"
        f"  author = {{{reference.author}}},\n"
        f"  title = {{{reference.title}}},\n"
        f"  journal = {{{reference.publication or ''}}},\n"
        f"  year = {{{reference.year}}}\n"
        "}"
    )

def format_book_reference(reference):
    return (
        f"@book{{{reference.citation_key},\n"
        f"  author = {{{reference.author}}},\n"
        f"  title = {{{reference.title}}},\n"
        f"  year = {{{reference.year}}},\n"
        f"  publisher = {{{reference.publication or ''}}}\n"
        "}"
    )
