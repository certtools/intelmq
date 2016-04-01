BEGIN;

/*
 Supported data formats like csv, iodef, etc.
*/
CREATE TABLE format (
    id INTEGER PRIMARY KEY,

    -- Most likely a WKT or MIME-Type
    name VARCHAR(80)
);


/*
  Organisation and Contact
*/
CREATE TABLE organisation (
    id INTEGER PRIMARY KEY,

    -- The name of the organisation.
    name VARCHAR(80),
    comment TEXT
);


CREATE TABLE contact (
    id INTEGER PRIMARY KEY,

    -- the email-address of the contact
    email VARCHAR(100),

    -- The data format to be used in emails sent to this contact.
    format_id INTEGER,

    -- Whether this contact tuple is maintained manually.
    is_manual BOOLEAN,

    comment TEXT,

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
    is_manual BOOLEAN,

    comment TEXT
);


-- A network
CREATE TABLE network (
    id INTEGER PRIMARY KEY,

    -- Network address as CIDR.
    address cidr,

    -- Whether this network tuple is maintained manually.
    is_manual BOOLEAN,

    comment TEXT
);


-- A fully qualified domain name
CREATE TABLE fqdn (
    id INTEGER PRIMARY KEY,

    -- The fully qualified domain name
    fqdn TEXT,

    -- Whether this FQDN-tuple is maintained manually.
    is_manual BOOLEAN,

    comment TEXT
);



/*
  Classifications of Events/Incidents
*/
CREATE TABLE classification_identifier (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

/*
 Template
*/
CREATE TABLE template (
    id INTEGER PRIMARY KEY,

    -- File-name of the template
    path VARCHAR(200),

    -- The classification identifier for which this template can be used.
    classification_identifier_id INTEGER,

    FOREIGN KEY (classification_identifier_id)
     REFERENCES classification_identifier (id)
);

/*
 Relations A_to_B
 Some of them (contact_to_X) carry an additional column TTL
*/
CREATE TABLE contact_to_asn (
    contact_id INTEGER,
    asn_id BIGINT,
    ttl INTEGER,

    PRIMARY KEY (contact_id, asn_id),

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (number),
    FOREIGN KEY (contact_id) REFERENCES contact (id)
);

CREATE TABLE contact_to_network (
    contact_id INTEGER,
    net_id INTEGER,
    ttl INTEGER,

    PRIMARY KEY (contact_id, net_id),

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (net_id) REFERENCES network (id)
);

CREATE TABLE contact_to_fqdn (
    contact_id INTEGER,
    fqdn_id INTEGER,
    ttl INTEGER,

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
    organisation_id INTEGER,
    template_id INTEGER,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);



-- Type for a single notification
CREATE TYPE notification AS (
    email VARCHAR(100),
    organisation VARCHAR(80),
    template_path VARCHAR(200),
    format_name VARCHAR(80),
    ttl INTEGER
);

-- Lookup all notifications for a given IP address and event
-- classification identifier
CREATE OR REPLACE FUNCTION
notifications_for_ip(ip INET, event_classification VARCHAR(100))
RETURNS SETOF notification
AS $$
BEGIN
    RETURN QUERY
    SELECT c.email, o.name, t.path, f.name, cn.ttl
      FROM organisation o
      JOIN contact_to_organisation co ON o.id = co.organisation_id
      JOIN contact c ON c.id = co.contact_id
      JOIN contact_to_network cn ON cn.contact_id = c.id
      JOIN network n ON cn.net_id = n.id
      JOIN organisation_to_template ot ON ot.organisation_id = o.id
      JOIN template t ON ot.template_id = t.id
      JOIN classification_identifier ci ON ci.id = t.id
      JOIN format f ON c.format_id = f.id
     WHERE n.address >> ip
       AND ci.name = event_classification;
END;
$$ LANGUAGE plpgsql VOLATILE;


COMMIT;
