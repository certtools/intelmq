BEGIN;


-- Email-Addresses
CREATE TABLE email (
    email_id SERIAL PRIMARY KEY,
    email VARCHAR(80)
);

CREATE TABLE asn_contact (
    asn INTEGER PRIMARY KEY,
    asn_contact_name VARCHAR(45)
);


CREATE TABLE nm_email_asn (
    email_id INTEGER,
    asn INTEGER,
    PRIMARY KEY (email_id, asn),

    FOREIGN KEY (email_id) REFERENCES email (email_id),
    FOREIGN KEY (asn) REFERENCES asn_contact (asn)
);



CREATE TABLE cidr_contact (
    cidr_contact_id SERIAL PRIMARY KEY,
    cidr_contact_name VARCHAR(45)
);

CREATE TABLE nm_email_cidr (
    email_id INTEGER,
    cidr_contact_id INTEGER,
    PRIMARY KEY (email_id, cidr_contact_id),

    FOREIGN KEY (email_id) REFERENCES email (email_id),
    FOREIGN KEY (cidr_contact_id) REFERENCES cidr_contact (cidr_contact_id)
);


CREATE TABLE cidr (
    cidr_id SERIAL PRIMARY KEY,
    cidr cidr,
    asn INTEGER,
    cidr_contact_id INTEGER,

    FOREIGN KEY (asn) REFERENCES asn_contact (asn),
    FOREIGN KEY (cidr_contact_id) REFERENCES cidr_contact (cidr_contact_id)
);

CREATE INDEX cidr_cidr_idx ON cidr (cidr);


COMMIT;
