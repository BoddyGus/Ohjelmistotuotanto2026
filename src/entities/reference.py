class Reference:
    def __init__(
        self, id, citation_key, reference_type,
        author, title, year, publication
    ):
        self.id = id
        self.citation_key = citation_key
        self.type = reference_type
        self.author = author
        self.title = title
        self.year = year
        self.publication = publication