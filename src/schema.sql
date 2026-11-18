CREATE TABLE bibliographic_references (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  citation_key TEXT NOT NULL UNIQUE,
  type TEXT NOT NULL,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  publication TEXT
);