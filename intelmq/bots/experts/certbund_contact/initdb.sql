BEGIN;

CREATE TABLE organisation (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80),
    comment TEXT
);

CREATE TABLE format (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80)
);

CREATE TABLE contact (
    id INTEGER PRIMARY KEY,
    email VARCHAR(100),
    format_id INTEGER,
    is_manual BOOLEAN,
    comment TEXT,

    FOREIGN KEY (format_id) REFERENCES format (id)
);

CREATE TABLE autonomous_system (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80),
    comment TEXT
);


CREATE TABLE etype (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80)
);

CREATE TABLE net (
    id INTEGER PRIMARY KEY,
    ip_start cidr,
    ip_end cidr,
    is_manual BOOLEAN
);
CREATE INDEX net_ip_start_idx ON net (ip_start);
CREATE INDEX net_ip_end_idx ON net (ip_end);

CREATE TABLE template (
    id INTEGER PRIMARY KEY,
    path VARCHAR(200),
    etype_id INTEGER,
    
    FOREIGN KEY (etype_id) REFERENCES etype (id)
);

CREATE TABLE contact_to_asn (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    asn_id INTEGER,

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (id),
    FOREIGN KEY (contact_id) REFERENCES contact (id)
);

CREATE TABLE contact_to_net (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    net_id INTEGER,

    FOREIGN KEY (contact_id) REFERENCES contact (id),
    FOREIGN KEY (net_id) REFERENCES net (id)
);

CREATE TABLE organisation_to_template (
    id INTEGER PRIMARY KEY,
    organisation_id INTEGER,
    template_id INTEGER,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id),
    FOREIGN KEY (template_id) REFERENCES template (id)
);



COMMIT;
