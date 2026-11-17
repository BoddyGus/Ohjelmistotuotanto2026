-- Temporary boilerplate table.
-- Keep it until the existing Todo application and tests are replaced.

CREATE TABLE todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  done BOOLEAN DEFAULT FALSE
);


CREATE TABLE bibliographic_references (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  citation_key TEXT NOT NULL UNIQUE,
  type TEXT NOT NULL,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  publication TEXT
);