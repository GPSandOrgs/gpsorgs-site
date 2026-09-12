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

-- ---- member registry (added 12 Sep 2026) ----
-- Applied with: wrangler d1 execute gpsorgs-signups --remote --file schema.sql
CREATE TABLE IF NOT EXISTS members (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  email         TEXT NOT NULL UNIQUE,      -- login email, stored lower case
  name          TEXT NOT NULL,
  affiliation   TEXT NOT NULL DEFAULT '',
  role          TEXT NOT NULL DEFAULT '',
  location      TEXT NOT NULL DEFAULT '',
  interests     TEXT NOT NULL DEFAULT '',
  email_private INTEGER NOT NULL DEFAULT 1, -- 1 = only the committee can see the email
  created       TEXT NOT NULL,
  updated       TEXT NOT NULL,
  last_login    TEXT
);
-- who carries a badge in the registry; maintained by hand (wrangler d1 execute)
CREATE TABLE IF NOT EXISTS badges (
  email  TEXT PRIMARY KEY,                 -- lower case
  badge  TEXT NOT NULL                     -- 'steering' | 'representative'
);
-- one-time sign-in codes; a row lives 15 minutes
CREATE TABLE IF NOT EXISTS login_codes (
  token     TEXT PRIMARY KEY,              -- random, kept in the gps_pending cookie
  email     TEXT NOT NULL,
  code_hash TEXT NOT NULL,                 -- sha256(token + code)
  attempts  INTEGER NOT NULL DEFAULT 0,
  created   TEXT NOT NULL,
  expires   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS login_codes_email ON login_codes (email);
-- long-lived sessions; the cookie holds the raw token, the table its hash
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY,
  email      TEXT NOT NULL,
  created    TEXT NOT NULL,
  expires    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_email ON sessions (email);
