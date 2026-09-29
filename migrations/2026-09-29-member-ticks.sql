-- Record each member's mailing-list and volunteer ticks on the members row.
-- Run once, before deploying the profile.js that writes these columns:
--   wrangler d1 execute gpsorgs-signups --remote --file migrations/2026-09-29-member-ticks.sql
ALTER TABLE members ADD COLUMN mailing INTEGER;    -- 1 ticked, 0 not, NULL unknown (registered before 29 Sep 2026)
ALTER TABLE members ADD COLUMN volunteer INTEGER;  -- 1 ticked, 0 not
-- backfill from signups: the volunteer flag is known; the mailing tick is known only for non-volunteers
UPDATE members SET volunteer = COALESCE((SELECT s.volunteer FROM signups s WHERE lower(s.email) = lower(members.email)), 0);
UPDATE members SET mailing = 1 WHERE volunteer = 0 AND lower(email) IN (SELECT lower(email) FROM signups);
UPDATE members SET mailing = 0 WHERE lower(email) NOT IN (SELECT lower(email) FROM signups);
