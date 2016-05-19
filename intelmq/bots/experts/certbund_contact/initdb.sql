BEGIN;

/*
 Supported data formats like csv, iodef, etc.
*/
CREATE TABLE format (
    id SERIAL PRIMARY KEY,

    -- Most likely a WKT or MIME-Type
    name VARCHAR(80) UNIQUE NOT NULL
);

/* Sector to classify organisations.
*/
CREATE TABLE sector (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

/*
  Organisation and Contact
*/
CREATE TABLE organisation (
    id SERIAL PRIMARY KEY,

    -- The name of the organisation.
    name VARCHAR(500) UNIQUE NOT NULL,

    -- The sector the organisation belongs to.
    sector_id INTEGER,

    comment TEXT NOT NULL DEFAULT '',

    -- The org: nic handle in the RIPE DB, if available
    ripe_org_hdl VARCHAR(100),

    -- The Trusted Introducer (TI) handle or URL: for example
    -- https://www.trusted-introducer.org/directory/teams/certat.html
    ti_handle    VARCHAR(500),

    -- The FIRST.org handle or URL: for example
    -- https://api.first.org/data/v1/teams?q=aconet-cert
    first_handle    VARCHAR(500),

    FOREIGN KEY (sector_id) REFERENCES sector(id)
);


CREATE TABLE organisation_automatic (
    id SERIAL PRIMARY KEY,

    name VARCHAR(500) UNIQUE NOT NULL,

    sector_id INTEGER,

    comment TEXT NOT NULL DEFAULT '',

    ripe_org_hdl VARCHAR(100),
    ti_handle    VARCHAR(500),
    first_handle VARCHAR(500),

    FOREIGN KEY (sector_id) REFERENCES sector(id)
);


CREATE TABLE contact (
    id SERIAL PRIMARY KEY,

    firstname VARCHAR (500) NOT NULL DEFAULT '',
    lastname  VARCHAR (500) NOT NULL DEFAULT '',
    tel       VARCHAR (500) NOT NULL DEFAULT '',

    pgp_key_id VARCHAR(128) NOT NULL DEFAULT '',

    -- the email-address of the contact
    email VARCHAR(100) NOT NULL,

    -- The data format to be used in emails sent to this contact.
    format_id INTEGER NOT NULL,

    comment TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (format_id) REFERENCES format (id)
);

CREATE TABLE contact_automatic (
    id INTEGER PRIMARY KEY,

    firstname VARCHAR (500) NOT NULL DEFAULT '',
    lastname  VARCHAR (500) NOT NULL DEFAULT '',
    tel       VARCHAR (500) NOT NULL DEFAULT '',

    pgp_key_id VARCHAR(128) NOT NULL DEFAULT '',

    -- the email-address of the contact
    email VARCHAR(100) NOT NULL,

    -- The data format to be used in emails sent to this contact.
    format_id INTEGER NOT NULL,

    comment TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (format_id) REFERENCES format (id)
);

-- Roles serve as an m-n relationship between organisations and contacts
CREATE TABLE role (
    id INTEGER PRIMARY KEY,

    -- free text for right now. We assume the regular tags from the
    -- RIPE DB such as "tech-c" or "abuse-c"
    -- possible values: "abuse-c", "billing-c" , "admin-c"
    role_type VARCHAR (500) NOT NULL default 'abuse-c',
    is_primary_contact BOOLEAN NOT NULL DEFAULT FALSE,

    organisation_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation(id),
    FOREIGN KEY (contact_id) REFERENCES contact(id)
);

-- Roles serve as an m-n relationship between organisations and contacts
CREATE TABLE role_automatic (
    id INTEGER PRIMARY KEY,

    role_type    VARCHAR (500) NOT NULL default 'abuse-c',
    is_primary_contact BOOLEAN NOT NULL DEFAULT FALSE,

    organisation_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic(id),
    FOREIGN KEY (contact_id) REFERENCES contact_automatic(id)
);


/*
  Network related tables, such as:
  AS, IP-Ranges, FQDN
*/

-- An autonomous system
CREATE TABLE autonomous_system (
    -- The atonomous system number
    number BIGINT PRIMARY KEY,

    -- RIPE handle (see
    -- https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/ripe-database-structure/3-1-list-of-primary-objects)
    -- and:
    -- https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-1-description-of-the-aut-num-object
    ripe_aut_num  VARCHAR(100),

    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX autonomous_system_number_idx ON autonomous_system (number);


CREATE TABLE autonomous_system_automatic (
    -- The atonomous system number
    number BIGINT PRIMARY KEY,

    ripe_aut_num  VARCHAR(100),

    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX autonomous_system_automatic_number_idx
    ON autonomous_system_automatic (number);


-- A network
-- See also: https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-4-description-of-the-inetnum-object
CREATE TABLE network (
    id SERIAL PRIMARY KEY,

    -- Network address as CIDR.
    address cidr UNIQUE NOT NULL,

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
--
-- XXX COMMENT Aaron: please let's simply depend on postgresql >= 9.4
-- IMHO that's okay to demand this XXX
--
CREATE INDEX network_cidr_lower_idx
          ON network ((host(network(address))));
CREATE INDEX network_cidr_upper_idx
          ON network ((host(broadcast(address))));


CREATE TABLE network_automatic (
    id INTEGER PRIMARY KEY,

    -- Network address as CIDR.
    address cidr UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX network_automatic_cidr_lower_idx
          ON network_automatic ((host(network(address))));
CREATE INDEX network_automatic_cidr_upper_idx
          ON network_automatic ((host(broadcast(address))));



-- A fully qualified domain name
CREATE TABLE fqdn (
    id SERIAL PRIMARY KEY,

    -- The fully qualified domain name
    fqdn TEXT UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX fqdn_fqdn_idx ON fqdn (fqdn);

CREATE TABLE fqdn_automatic (
    id INTEGER PRIMARY KEY,

    -- The fully qualified domain name
    fqdn TEXT UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX fqdn_automatic_fqdn_idx ON fqdn (fqdn);


/*
  Classifications of Events/Incidents
*/
CREATE TABLE classification_identifier (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE INDEX classification_identifier_name_idx
          ON classification_identifier (name);

/*
 Template
*/
CREATE TABLE template (
    id SERIAL PRIMARY KEY,

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
 See also https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/ripe-database-structure/3-1-list-of-primary-objects
*/
CREATE TABLE organisation_to_asn (
    organisation_id INTEGER,
    asn_id BIGINT,
    notification_interval INTEGER NOT NULL, -- interval in seconds

    PRIMARY KEY (organisation_id, asn_id),

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (number),
    FOREIGN KEY (organisation_id) REFERENCES organisation (id)
);


CREATE TABLE organisation_to_asn_automatic (
    organisation_id INTEGER,
    asn_id BIGINT,
    notification_interval INTEGER NOT NULL, -- interval in seconds

    PRIMARY KEY (organisation_id, asn_id),

    FOREIGN KEY (asn_id) REFERENCES autonomous_system_automatic (number),
    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id)
);


CREATE TABLE organisation_to_network (
    organisation_id INTEGER,
    net_id INTEGER,
    notification_interval INTEGER NOT NULL, -- interval in seconds

    PRIMARY KEY (organisation_id, net_id),

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (net_id) REFERENCES network (id)
);

CREATE TABLE organisation_to_network_automatic (
    organisation_id INTEGER,
    net_id INTEGER,
    notification_interval INTEGER NOT NULL, -- interval in seconds

    PRIMARY KEY (organisation_id, net_id),

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id),
    FOREIGN KEY (net_id) REFERENCES network_automatic (id)
);


CREATE TABLE organisation_to_fqdn (
    organisation_id INTEGER,
    fqdn_id INTEGER,
    notification_interval INTEGER NOT NULL,

    PRIMARY KEY (organisation_id, fqdn_id),

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (fqdn_id) REFERENCES fqdn (id)
);

CREATE TABLE organisation_to_fqdn_automatic (
    organisation_id INTEGER,
    fqdn_id INTEGER,
    notification_interval INTEGER NOT NULL,

    PRIMARY KEY (organisation_id, fqdn_id),

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id),
    FOREIGN KEY (fqdn_id) REFERENCES fqdn_automatic (id)
);


CREATE TABLE organisation_to_contact (
    contact_id INTEGER,
    organisation_id INTEGER,

    PRIMARY KEY (contact_id, organisation_id),

    is_primary_contact BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (organisation_id) REFERENCES organisation (id)
);

CREATE TABLE organisation_to_contact_automatic (
    contact_id INTEGER,
    organisation_id INTEGER,

    PRIMARY KEY (contact_id, organisation_id),

    is_primary_contact BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (contact_id) REFERENCES contact_automatic (id),
    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id)
);


CREATE TABLE organisation_to_template (
    id SERIAL PRIMARY KEY,
    organisation_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);

CREATE INDEX organisation_to_template_organisation_idx
          ON organisation_to_template (organisation_id);
CREATE INDEX organisation_to_template_template_idx
          ON organisation_to_template (template_id);


CREATE TABLE organisation_to_template_automatic (
    id SERIAL PRIMARY KEY,
    organisation_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);

CREATE INDEX organisation_to_template_automatic_organisation_idx
          ON organisation_to_template_automatic (organisation_id);
CREATE INDEX organisation_to_template_automatic_template_idx
          ON organisation_to_template_automatic (template_id);


-- Type for a single notification
CREATE TYPE notification AS (
    email VARCHAR(100),
    organisation VARCHAR(500),
    template_path VARCHAR(200),
    format_name VARCHAR(80),
    notification_interval INTEGER
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
SELECT oc.contact_id, o.name, t.path, ci.name
  FROM organisation_to_contact AS oc
  JOIN organisation AS o ON o.id = oc.organisation_id
  JOIN organisation_to_template AS ot ON ot.organisation_id = o.id
  JOIN template AS t ON ot.template_id = t.id
  JOIN classification_identifier AS ci
    ON ci.id = t.classification_identifier_id;


CREATE OR REPLACE VIEW contact_organisation_settings_automatic (
    contact_id,
    organisation_name,
    template_path,
    classification_identifier
) AS
SELECT oc.contact_id, o.name, t.path, ci.name
  FROM organisation_to_contact_automatic AS oc
  JOIN organisation_automatic AS o ON o.id = oc.organisation_id
  JOIN organisation_to_template_automatic AS ot ON ot.organisation_id = o.id
  JOIN template AS t ON ot.template_id = t.id
  JOIN classification_identifier AS ci
    ON ci.id = t.classification_identifier_id;


-- Lookup all notifications for a given IP address and event
-- classification identifier
CREATE OR REPLACE FUNCTION
notifications_for_ip(event_ip INET, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id,
                             notification_interval)
        AS (SELECT c.id, c.email, c.format_id, orgn.notification_interval
              FROM contact c
              JOIN organisation_to_contact AS oc ON oc.contact_id = c.id
              JOIN organisation_to_network AS orgn
                ON orgn.organisation_id = oc.organisation_id
              JOIN network AS n ON n.id = orgn.net_id
             WHERE host(network(n.address)) <= host(event_ip)
               AND host(event_ip) <= host(broadcast(n.address)))
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts mc
      JOIN contact_organisation_settings AS cos
        ON mc.contact_id = cos.contact_id
      JOIN format f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


CREATE OR REPLACE FUNCTION
notifications_for_ip_automatic(event_ip INET,
                               event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id,
                             notification_interval)
        AS (SELECT c.id, c.email, c.format_id, orgn.notification_interval
              FROM contact_automatic c
              JOIN organisation_to_contact_automatic AS oc
                ON oc.contact_id = c.id
              JOIN organisation_to_network_automatic AS orgn
                ON orgn.organisation_id = oc.organisation_id
              JOIN network_automatic AS n ON n.id = orgn.net_id
             WHERE host(network(n.address)) <= host(event_ip)
               AND host(event_ip) <= host(broadcast(n.address)))
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts mc
      JOIN contact_organisation_settings_automatic AS cos
        ON mc.contact_id = cos.contact_id
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
      WITH matched_contacts (contact_id, email, format_id,
                             notification_interval)
        AS (SELECT c.id, c.email, c.format_id, orga.notification_interval
              FROM contact AS c
              JOIN organisation_to_contact AS oc ON oc.contact_id = c.id
              JOIN organisation_to_asn AS orga
                ON orga.organisation_id = oc.organisation_id
              JOIN autonomous_system AS a ON a.number = orga.asn_id
             WHERE a.number = event_asn)
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN contact_organisation_settings AS cos
        ON mc.contact_id = cos.contact_id
      JOIN format AS f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE FUNCTION
notifications_for_asn_automatic(event_asn BIGINT,
                                event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id,
                             notification_interval)
        AS (SELECT c.id, c.email, c.format_id, orga.notification_interval
              FROM contact_automatic AS c
              JOIN organisation_to_contact_automatic AS oc
                ON oc.contact_id = c.id
              JOIN organisation_to_asn_automatic AS orga
                ON orga.organisation_id = oc.organisation_id
              JOIN autonomous_system_automatic AS a ON a.number = orga.asn_id
             WHERE a.number = event_asn)
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN contact_organisation_settings_automatic AS cos
        ON mc.contact_id = cos.contact_id
      JOIN format AS f ON mc.format_id = f.id
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
      WITH matched_contacts (contact_id, email, format_id, notification_interval)
        AS (SELECT c.id, c.email, c.format_id, orgf.notification_interval
              FROM contact AS c
              JOIN organisation_to_contact AS oc ON oc.contact_id = c.id
              JOIN organisation_to_fqdn AS orgf
                ON orgf.organisation_id = oc.organisation_id
              JOIN fqdn AS f ON f.id = orgf.fqdn_id
             WHERE f.fqdn = event_fqdn)
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN contact_organisation_settings AS cos
        ON mc.contact_id = cos.contact_id
      JOIN format AS f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE FUNCTION
notifications_for_fqdn_automatic(event_fqdn TEXT,
                                 event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (contact_id, email, format_id,
                             notification_interval)
        AS (SELECT c.id, c.email, c.format_id, orgf.notification_interval
              FROM contact_automatic AS c
              JOIN organisation_to_contact_automatic AS oc
                ON oc.contact_id = c.id
              JOIN organisation_to_fqdn_automatic AS orgf
                ON orgf.organisation_id = oc.organisation_id
              JOIN fqdn_automatic AS f ON f.id = orgf.fqdn_id
             WHERE f.fqdn = event_fqdn)
    SELECT mc.email, cos.organisation_name, cos.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN contact_organisation_settings_automatic AS cos
        ON mc.contact_id = cos.contact_id
      JOIN format AS f ON mc.format_id = f.id
     WHERE cos.classification_identifier = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


COMMIT;
