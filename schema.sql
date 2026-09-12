-- Signups from the join form on gpsorgs.com. Applied once with:
--   wrangler d1 execute gpsorgs-signups --remote --file schema.sql
CREATE TABLE IF NOT EXISTS signups (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ts          TEXT NOT NULL,            -- ISO 8601 UTC, set by the function
  name        TEXT NOT NULL,
  email       TEXT NOT NULL,
  affiliation TEXT NOT NULL DEFAULT '',
  interests   TEXT NOT NULL DEFAULT '',
  consent     INTEGER NOT NULL DEFAULT 1
);
CREATE UNIQUE INDEX IF NOT EXISTS signups_email ON signups (lower(email));
