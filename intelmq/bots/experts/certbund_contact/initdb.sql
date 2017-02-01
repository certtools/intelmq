BEGIN;

/*
 Template table containing with elements for automatic tables 
 */
CREATE TEMP TABLE automatic_templ (
    import_source VARCHAR(500) NOT NULL CHECK (import_source <> ''),
    import_time TIMESTAMP NOT NULL
);

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

    -- In the ripe db there are names identical for more than one
    -- organisation, so we can not make this key unique.
    name VARCHAR(500) NOT NULL,

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
    LIKE automatic_templ INCLUDING ALL,
    LIKE organisation INCLUDING ALL,

    FOREIGN KEY (sector_id) REFERENCES sector(id)
);


CREATE TABLE contact (
    id SERIAL PRIMARY KEY,

    firstname VARCHAR (500) NOT NULL DEFAULT '',
    lastname  VARCHAR (500) NOT NULL DEFAULT '',
    tel       VARCHAR (500) NOT NULL DEFAULT '',

    -- The full fingerprint of the OpenPGP pubkey of the contact as GnuPG
    -- would accept it to specify a user ID.
    -- (This avoids ambiguities in case that there are duplicated key IDs.)
    openpgp_fpr VARCHAR(128) NOT NULL DEFAULT '',

    -- the email-address of the contact
    email VARCHAR(100) NOT NULL,

    -- The data format to be used in emails sent to this contact.
    format_id INTEGER NOT NULL,

    comment TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (format_id) REFERENCES format (id)
);

CREATE TABLE contact_automatic (
    LIKE automatic_templ INCLUDING ALL,
    LIKE contact INCLUDING ALL,

    FOREIGN KEY (format_id) REFERENCES format (id)
);

-- Roles serve as an m-n relationship between organisations and contacts
CREATE TABLE role (
    id SERIAL PRIMARY KEY,

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
    LIKE automatic_templ INCLUDING ALL,
    LIKE role INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic(id),
    FOREIGN KEY (contact_id) REFERENCES contact_automatic(id)
);


-- create indices on role after role_automatic has been created to avoid
-- duplication of indices due to the "LIKE role INCLUDING ALL" in the
-- CREATE TABLE statement for role_automatic.
CREATE INDEX role_organisation_id_idx
          ON role (organisation_id);
CREATE INDEX role_contact_id_idx
          ON role (contact_id);


CREATE INDEX role_automatic_organisation_id_idx
          ON role_automatic (organisation_id);
CREATE INDEX role_automatic_contact_id_idx
          ON role_automatic (contact_id);


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


CREATE TABLE autonomous_system_automatic (
    LIKE automatic_templ INCLUDING ALL,
    LIKE autonomous_system INCLUDING ALL
);


-- A network
-- See also: https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-4-description-of-the-inetnum-object
CREATE TABLE network (
    id SERIAL PRIMARY KEY,

    -- Network address as CIDR.
    address cidr UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);

CREATE TABLE network_automatic (
    LIKE automatic_templ INCLUDING ALL,
    LIKE network INCLUDING ALL
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
--   inet(host(network(n.address))) <= ip
--   AND ip <= inet(host(broadcast(n.address)))
--
-- FIXME: In PostgreSQL 9.4 there's GiST indexes for the inet and cidr
-- types (see http://www.postgresql.org/docs/9.4/static/release-9-4.html).
-- We cannot use that at the moment, because we still need to support
-- PostgreSQL 9.3 which is the version available in Ubuntu 14.04LTS.
--
-- XXX COMMENT Aaron: please let's simply depend on postgresql >= 9.4
-- IMHO that's okay to demand this XXX
--
CREATE INDEX network_cidr_lower_idx
          ON network ((inet(host(network(address)))));
CREATE INDEX network_cidr_upper_idx
          ON network ((inet(host(broadcast(address)))));

CREATE INDEX network_automatic_cidr_lower_idx
          ON network_automatic ((inet(host(network(address)))));
CREATE INDEX network_automatic_cidr_upper_idx
          ON network_automatic ((inet(host(broadcast(address)))));



-- A fully qualified domain name
CREATE TABLE fqdn (
    id SERIAL PRIMARY KEY,

    -- The fully qualified domain name
    fqdn TEXT UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE fqdn_automatic (
    LIKE automatic_templ INCLUDING ALL,
    LIKE fqdn INCLUDING ALL
);



/*
  Classifications of Events/Incidents
*/
CREATE TABLE classification_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE classification_identifier (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

/*
 Template
*/
CREATE TABLE template (
    id SERIAL PRIMARY KEY,

    -- File-name of the template
    path VARCHAR(200) NOT NULL,

    -- The classification type for which this template can be used.
    classification_type_id INTEGER NOT NULL,

    FOREIGN KEY (classification_type_id)
     REFERENCES classification_type (id)
);

CREATE INDEX template_classification_idx
          ON template (classification_type_id);

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
    LIKE automatic_templ INCLUDING ALL,
    LIKE organisation_to_asn INCLUDING ALL,

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
    LIKE automatic_templ INCLUDING ALL,
    LIKE organisation_to_network INCLUDING ALL,

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
    LIKE automatic_templ INCLUDING ALL,
    LIKE organisation_to_fqdn INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id),
    FOREIGN KEY (fqdn_id) REFERENCES fqdn_automatic (id)
);


CREATE TABLE organisation_to_template (
    id SERIAL PRIMARY KEY,
    organisation_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);

CREATE TABLE organisation_to_template_automatic (
    LIKE automatic_templ INCLUDING ALL,
    LIKE organisation_to_template INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);


CREATE INDEX organisation_to_template_organisation_idx
          ON organisation_to_template (organisation_id);
CREATE INDEX organisation_to_template_template_idx
          ON organisation_to_template (template_id);

CREATE INDEX organisation_to_template_automatic_organisation_idx
          ON organisation_to_template_automatic (organisation_id);
CREATE INDEX organisation_to_template_automatic_template_idx
          ON organisation_to_template_automatic (template_id);


-- Inhibit notifications

CREATE TABLE inhibition (
    id SERIAL PRIMARY KEY,

    asn_id BIGINT,
    net_id INTEGER,

    classification_type_id INTEGER,
    classification_identifier_id INTEGER,

    comment TEXT NOT NULL DEFAULT '',

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (number),
    FOREIGN KEY (net_id) REFERENCES network (id),

    FOREIGN KEY (classification_type_id)
     REFERENCES classification_type (id),
    FOREIGN KEY (classification_identifier_id)
     REFERENCES classification_identifier (id),

    CHECK (asn_id IS NOT NULL OR net_id IS NOT NULL)
);


-- Determine whether notifications are inhibited for the event.
-- Notifications are inhibited if a matching entry exists in inhibition.
CREATE OR REPLACE FUNCTION
notifications_inhibited(event_asn BIGINT, event_ip INET,
                        event_classification_type TEXT,
                        event_classification_identifier TEXT)
RETURNS BOOLEAN
AS $$
BEGIN
    RETURN EXISTS (
       SELECT * FROM inhibition
        WHERE (asn_id IS NULL OR asn_id = event_asn)
          AND (net_id IS NULL
               OR net_id = (SELECT n.id FROM network n
                             WHERE inet(host(network(n.address))) <= event_ip
                               AND event_ip <= inet(host(broadcast(n.address)))))
          AND (classification_type_id IS NULL
	       OR classification_type_id
	        = (SELECT id FROM classification_type c
                    WHERE c.name = event_classification_type))
          AND (classification_identifier_id IS NULL
	       OR classification_identifier_id
	        = (SELECT id FROM classification_identifier c
                    WHERE c.name = event_classification_identifier)));
END;
$$ LANGUAGE plpgsql VOLATILE;



-- Type for a single notification
CREATE TYPE notification AS (
    email VARCHAR(100),
    organisation VARCHAR(500),
    sector VARCHAR(100),
    template_path VARCHAR(200),
    format_name VARCHAR(80),
    notification_interval INTEGER
);


-- View combining the information about organisations and their
-- associated templates for easy combination with the organisation_to_*
-- tables for IP, FQDN and ASN.
CREATE OR REPLACE VIEW organisation_settings (
    organisation_id,
    organisation_name,
    sector,
    template_path,
    classification_type
) AS
SELECT o.id, o.name, s.name, t.path, ci.name
  FROM organisation AS o
  LEFT OUTER JOIN sector AS s on s.id = o.sector_id
  JOIN organisation_to_template AS ot ON ot.organisation_id = o.id
  JOIN template AS t ON ot.template_id = t.id
  JOIN classification_type AS ci
    ON ci.id = t.classification_type_id;


CREATE OR REPLACE VIEW organisation_settings_automatic (
    organisation_id,
    organisation_name,
    sector,
    template_path,
    classification_type
) AS
SELECT o.id, o.name, s.name, t.path, ct.name
  FROM organisation_automatic AS o
  LEFT OUTER JOIN sector AS s on s.id = o.sector_id
  JOIN organisation_to_template_automatic AS ot ON ot.organisation_id = o.id
  JOIN template AS t ON ot.template_id = t.id
  JOIN classification_type AS ct
    ON ct.id = t.classification_type_id;


-- Lookup all notifications for a given IP address and event
-- classification type
CREATE OR REPLACE FUNCTION
notifications_for_ip(event_ip INET, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (email, format_id, notification_interval,
                             organisation_id)
        AS (SELECT c.email, c.format_id, orgn.notification_interval,
                   r.organisation_id
              FROM contact c
              JOIN role AS r ON r.contact_id = c.id
              JOIN organisation_to_network AS orgn
                ON orgn.organisation_id = r.organisation_id
              JOIN network AS n ON n.id = orgn.net_id
             WHERE inet(host(network(n.address))) <= event_ip
               AND event_ip <= inet(host(broadcast(n.address))))
    SELECT mc.email, os.organisation_name, os.sector, os.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts mc
      JOIN organisation_settings AS os
        ON mc.organisation_id = os.organisation_id
      JOIN format f ON mc.format_id = f.id
     WHERE os.classification_type = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


CREATE OR REPLACE FUNCTION
notifications_for_ip_automatic(event_ip INET,
                               event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (email, format_id, notification_interval,
                             organisation_id)
        AS (SELECT c.email, c.format_id, orgn.notification_interval,
                   r.organisation_id
              FROM contact_automatic c
              JOIN role_automatic AS r ON r.contact_id = c.id
              JOIN organisation_to_network_automatic AS orgn
                ON orgn.organisation_id = r.organisation_id
              JOIN network_automatic AS n ON n.id = orgn.net_id
             WHERE inet(host(network(n.address))) <= event_ip
               AND event_ip <= inet(host(broadcast(n.address))))
    SELECT mc.email, os.organisation_name, os.sector, os.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts mc
      JOIN organisation_settings_automatic AS os
        ON mc.organisation_id = os.organisation_id
      JOIN format f ON mc.format_id = f.id
     WHERE os.classification_type = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


-- Lookup all notifications for a given ASN and event classification
-- type
CREATE OR REPLACE FUNCTION
notifications_for_asn(event_asn BIGINT, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (email, format_id, notification_interval,
                             organisation_id)
        AS (SELECT c.email, c.format_id, orga.notification_interval,
                   r.organisation_id
              FROM contact AS c
              JOIN role AS r ON r.contact_id = c.id
              JOIN organisation_to_asn AS orga
                ON orga.organisation_id = r.organisation_id
              JOIN autonomous_system AS a ON a.number = orga.asn_id
             WHERE a.number = event_asn)
    SELECT mc.email, os.organisation_name, os.sector, os.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts mc
      JOIN organisation_settings AS os
        ON mc.organisation_id = os.organisation_id
      JOIN format f ON mc.format_id = f.id
     WHERE os.classification_type = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE FUNCTION
notifications_for_asn_automatic(event_asn BIGINT,
                                event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (email, format_id, notification_interval,
                             organisation_id)
        AS (SELECT c.email, c.format_id, orga.notification_interval,
                   r.organisation_id
              FROM contact_automatic AS c
              JOIN role_automatic AS r ON r.contact_id = c.id
              JOIN organisation_to_asn_automatic AS orga
                ON orga.organisation_id = r.organisation_id
              JOIN autonomous_system_automatic AS a ON a.number = orga.asn_id
             WHERE a.number = event_asn)
    SELECT mc.email, os.organisation_name, os.sector, os.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN organisation_settings_automatic AS os
        ON mc.organisation_id = os.organisation_id
      JOIN format AS f ON mc.format_id = f.id
     WHERE os.classification_type = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;

-- Lookup all notifications for a given FQDN and event classification
-- type
CREATE OR REPLACE FUNCTION
notifications_for_fqdn(event_fqdn TEXT, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (email, format_id, notification_interval,
                             organisation_id)
        AS (SELECT c.email, c.format_id, orgf.notification_interval,
                   r.organisation_id
              FROM contact AS c
              JOIN role AS r ON r.contact_id = c.id
              JOIN organisation_to_fqdn AS orgf
                ON orgf.organisation_id = r.organisation_id
              JOIN fqdn AS f ON f.id = orgf.fqdn_id
             WHERE f.fqdn = event_fqdn)
    SELECT mc.email, os.organisation_name, os.sector, os.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN organisation_settings AS os
        ON mc.organisation_id = os.organisation_id
      JOIN format AS f ON mc.format_id = f.id
     WHERE os.classification_type = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE FUNCTION
notifications_for_fqdn_automatic(event_fqdn TEXT,
                                 event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
      WITH matched_contacts (email, format_id, notification_interval,
                             organisation_id)
        AS (SELECT c.email, c.format_id, orgf.notification_interval,
                   r.organisation_id
              FROM contact_automatic AS c
              JOIN role_automatic AS r ON r.contact_id = c.id
              JOIN organisation_to_fqdn_automatic AS orgf
                ON orgf.organisation_id = r.organisation_id
              JOIN fqdn_automatic AS f ON f.id = orgf.fqdn_id
             WHERE f.fqdn = event_fqdn)
    SELECT mc.email, os.organisation_name, os.sector, os.template_path, f.name,
           mc.notification_interval
      FROM matched_contacts AS mc
      JOIN organisation_settings_automatic AS os
        ON mc.organisation_id = os.organisation_id
      JOIN format AS f ON mc.format_id = f.id
     WHERE os.classification_type = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


COMMIT;
