-- SPDX-FileCopyrightText: 2020 Sebastian Wagner
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

-- create a table to save the information
CREATE TABLE meta (
    "oldest_time.source" TIMESTAMP WITH TIME ZONE NULL
);
INSERT INTO meta VALUES ('2300-01-01T00:00:00+00');

-- create the trigger function comparing the new data with the known oldest data
CREATE OR REPLACE FUNCTION update_oldest_time_source () RETURNS TRIGGER
AS $$
BEGIN
IF (SELECT "oldest_time.source" FROM meta) > NEW."time.source"
THEN
UPDATE meta SET "oldest_time.source" = NEW."time.source";
END IF;
RETURN NEW;
END;
$$
LANGUAGE plpgsql
VOLATILE;

-- create the trigger
CREATE CONSTRAINT TRIGGER tr_oldest_time_source
AFTER INSERT OR UPDATE ON events
DEFERRABLE
FOR EACH ROW
EXECUTE PROCEDURE update_oldest_time_source();

-- query with:
SELECT "oldest_time.source" FROM meta;
