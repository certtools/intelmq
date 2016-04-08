BEGIN;

/*
 Supported data formats like csv, iodef, etc.
*/
CREATE TABLE format (
    id INTEGER PRIMARY KEY,

    -- Most likely a WKT or MIME-Type
    name VARCHAR(80) UNIQUE NOT NULL
);


/*
  Organisation and Contact
*/
CREATE TABLE organisation (
    id INTEGER PRIMARY KEY,

    -- The name of the organisation.
    name VARCHAR(80) UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE contact (
    id INTEGER PRIMARY KEY,

    -- the email-address of the contact
    email VARCHAR(100) NOT NULL,

    -- The data format to be used in emails sent to this contact.
    format_id INTEGER NOT NULL,

    -- Whether this contact tuple is maintained manually.
    is_manual BOOLEAN NOT NULL,

    comment TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (format_id) REFERENCES format (id)
);

/*
  Network related tables, such as:
  AS, IP-Ranges, FQDN
*/

-- An autonomous system
CREATE TABLE autonomous_system (
    -- The atonomous system number
    number BIGINT PRIMARY KEY,

    -- Whether this autonomous system tuple is maintained manually.
    is_manual BOOLEAN NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);

CREATE INDEX autonomous_system_number_idx ON autonomous_system (number);


-- A network
CREATE TABLE network (
    id INTEGER PRIMARY KEY,

    -- Network address as CIDR.
    address cidr UNIQUE NOT NULL,

    -- Whether this network tuple is maintained manually.
    is_manual BOOLEAN NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);

-- Indexes on the cidr column to improve queries that look up a network
-- based on an IP-address. The default btree index of PostgreSQL is not
-- used for those queries, so we need to do it in some other way. A
-- simple way is to have indexes for the lower and upper bounds of the
-- address range represented by the cidr value, so that's what we do
-- here. The main downside is that the queries will have to use the same
-- expressions as the ones used in the indexes. E.g. a query matching
-- network that contain the IP-address ip and using n as the local alias
-- for the table should use a where clause condition of the form
--
--   host(network(n.address)) <= ip AND ip <= host(broadcast(n.address))
--
-- FIXME: In PostgreSQL 9.4 there's GiST indexes for the intet and cidr
-- types (see http://www.postgresql.org/docs/9.4/static/release-9-4.html).
-- We cannot use that at the moment, because we still need to support
-- PostgreSQL 9.3 which is the version available in Ubuntu 14.04LTS.
CREATE INDEX network_cidr_lower_idx
          ON network ((host(network(address))));
CREATE INDEX network_cidr_upper_idx
          ON network ((host(broadcast(address))));


-- A fully qualified domain name
CREATE TABLE fqdn (
    id INTEGER PRIMARY KEY,

    -- The fully qualified domain name
    fqdn TEXT UNIQUE NOT NULL,

    -- Whether this FQDN-tuple is maintained manually.
    is_manual BOOLEAN NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);

CREATE INDEX fqdn_fqdn_idx ON fqdn (fqdn);


/*
  Classifications of Events/Incidents
*/
CREATE TABLE classification_identifier (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE INDEX classification_identifier_name_idx
          ON classification_identifier (name);

/*
 Template
*/
CREATE TABLE template (
    id INTEGER PRIMARY KEY,

    -- File-name of the template
    path VARCHAR(200) NOT NULL,

    -- The classification identifier for which this template can be used.
    classification_identifier_id INTEGER NOT NULL,

    FOREIGN KEY (classification_identifier_id)
     REFERENCES classification_identifier (id)
);

CREATE INDEX template_classification_idx
          ON template (classification_identifier_id);

/*
 Relations A_to_B
 Some of them (contact_to_X) carry an additional column TTL
*/
CREATE TABLE contact_to_asn (
    contact_id INTEGER,
    asn_id BIGINT,
    ttl INTEGER NOT NULL,

    PRIMARY KEY (contact_id, asn_id),

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (number),
    FOREIGN KEY (contact_id) REFERENCES contact (id)
);

CREATE TABLE contact_to_network (
    contact_id INTEGER,
    net_id INTEGER,
    ttl INTEGER NOT NULL,

    PRIMARY KEY (contact_id, net_id),

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (net_id) REFERENCES network (id)
);

CREATE TABLE contact_to_fqdn (
    contact_id INTEGER,
    fqdn_id INTEGER,
    ttl INTEGER NOT NULL,

    PRIMARY KEY (contact_id, fqdn_id),

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (fqdn_id) REFERENCES fqdn (id)
);


CREATE TABLE contact_to_organisation (
    contact_id INTEGER,
    organisation_id INTEGER,

    PRIMARY KEY (contact_id, organisation_id),

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (organisation_id) REFERENCES organisation (id)
);

CREATE TABLE organisation_to_template (
    id INTEGER PRIMARY KEY,
    organisation_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);

CREATE INDEX organisation_to_template_organisation_idx
          ON organisation_to_template (organisation_id);
CREATE INDEX organisation_to_template_template_idx
          ON organisation_to_template (template_id);


-- Type for a single notification
CREATE TYPE notification AS (
    email VARCHAR(100),
    organisation VARCHAR(80),
    template_path VARCHAR(200),
    format_name VARCHAR(80),
    ttl INTEGER
);


-- View combining the information about organisations and their
-- associated templates for easy combination with the contact_to_*
-- tables.
CREATE OR REPLACE VIEW contact_organisation_settings (
    contact_id,
    organisation_name,
    template_path,
    classification_identifier
) AS
SELECT co.contact_id, o.name, t.path, ci.name
  FROM contact_to_organisation co
  JOIN organisation o ON o.id = co.organisation_id
  JOIN organisation_to_template ot ON ot.organisation_id = o.id
  JOIN template t ON ot.template_id = t.id
  JOIN classification_identifier ci
    ON ci.id = t.classification_identifier_id;


-- Lookup all notifications for a given IP address and event
-- classification identifier
CREATE OR REPLACE FUNCTION
notifications_for_ip(event_ip INET, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id, ttl)
        AS (SELECT c.id, c.email, c.format_id, cn.ttl
              FROM contact c
              JOIN contact_to_network cn ON cn.contact_id = c.id
              JOIN network n ON n.id = cn.net_id
             WHERE host(network(n.address)) <= host(event_ip)
               AND host(event_ip) <= host(broadcast(n.address)))
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name, mc.ttl
      FROM matched_contacts mc
      JOIN contact_organisation_settings cos ON mc.contact_id = cos.contact_id
      JOIN format f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Lookup all notifications for a given ASN and event classification
-- identifier
CREATE OR REPLACE FUNCTION
notifications_for_asn(event_asn BIGINT, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id, ttl)
        AS (SELECT c.id, c.email, c.format_id, ca.ttl
              FROM contact c
              JOIN contact_to_asn ca ON ca.contact_id = c.id
              JOIN autonomous_system a ON a.number = ca.asn_id
             WHERE a.number = event_asn)
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name, mc.ttl
      FROM matched_contacts mc
      JOIN contact_organisation_settings cos ON mc.contact_id = cos.contact_id
      JOIN format f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Lookup all notifications for a given FQDN and event classification
-- identifier
CREATE OR REPLACE FUNCTION
notifications_for_fqdn(event_fqdn TEXT, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id, ttl)
        AS (SELECT c.id, c.email, c.format_id, cd.ttl
              FROM contact c
              JOIN contact_to_fqdn cd ON cd.contact_id = c.id
              JOIN fqdn f ON f.id = cd.fqdn_id
             WHERE f.fqdn = event_fqdn)
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name, mc.ttl
      FROM matched_contacts mc
      JOIN contact_organisation_settings cos ON mc.contact_id = cos.contact_id
      JOIN format f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


COMMIT;
