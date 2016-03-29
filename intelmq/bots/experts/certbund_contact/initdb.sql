BEGIN;

/*
 Format
 csv, iodef, etc..
*/
CREATE TABLE format (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80) -- Most likely a WKT or MIME-Type
);

/*
  Organisation and Contact
*/
CREATE TABLE organisation (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80),
    comment TEXT
);

CREATE TABLE contact (
    id INTEGER PRIMARY KEY,
    email VARCHAR(100),
    format_id INTEGER, -- Which format has to be used for this contact?
    is_manual BOOLEAN, -- Was the contact added manually? This should be true, then.
    comment TEXT,

    FOREIGN KEY (format_id) REFERENCES format (id)
);

/*
  Network related tables, such as:
  AS, IP-Ranges, FQDN
*/
CREATE TABLE autonomous_system (
    id INTEGER PRIMARY KEY,
    number INTEGER, -- Whe skip the 'AS' here.
    is_manual BOOLEAN,
    comment TEXT
);


CREATE TABLE network (
    id INTEGER PRIMARY KEY,
    ip_start cidr, -- Why CIDR ?
    ip_end cidr, -- Why CIDR ?
    is_manual BOOLEAN,
    comment TEXT
);
-- Indices on IPs
CREATE INDEX net_ip_start_idx ON network (ip_start);
CREATE INDEX net_ip_end_idx ON network (ip_end);


CREATE TABLE fqdn (
    id INTEGER PRIMARY KEY,
    fqdn TEXT, -- TODO Should an index exist?
    is_manual BOOLEAN,
    comment TEXT
);



/*
  Classifications of Events/Incidents
*/
CREATE TABLE classification_taxonomy (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE classification_type (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE classification_identifier (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

/*
 Template
*/
CREATE TABLE template (
    id INTEGER PRIMARY KEY,
    path VARCHAR(200),
    classification_identifier_id INTEGER, -- For which Incident should this template be used?

    FOREIGN KEY (classification_identifier_id) REFERENCES classification_identifier (id)
);

/*
 Relations A_to_B
 Some of them (contact_to_X) carry an additional column TTL
*/
CREATE TABLE contact_to_asn (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    asn_id INTEGER,
    ttl INTEGER,

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (id),
    FOREIGN KEY (contact_id) REFERENCES contact (id)
);

CREATE TABLE contact_to_network (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    net_id INTEGER,
    ttl INTEGER,

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (net_id) REFERENCES network (id)
);

CREATE TABLE contact_to_fqdn (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    fqdn_id INTEGER,
    ttl INTEGER,

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (fqdn_id) REFERENCES fqdn (id)
);

CREATE TABLE organisation_to_template (
    id INTEGER PRIMARY KEY,
    organisation_id INTEGER,
    template_id INTEGER,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);

CREATE TABLE classification_type_to_taxonomy (
    id INTEGER PRIMARY KEY,
    type_id INTEGER,
    taxonomy_id INTEGER,

    FOREIGN KEY (taxonomy_id) REFERENCES classification_taxonomy (id),
    FOREIGN KEY (type_id) REFERENCES classification_type (id)
);

CREATE TABLE classification_identifier_to_type (
    id INTEGER PRIMARY KEY,
    identifier_id INTEGER,
    type_id INTEGER,

    FOREIGN KEY (identifier_id) REFERENCES classification_identifier (id),
    FOREIGN KEY (type_id) REFERENCES classification_type (id)
);

COMMIT;
