BEGIN;

/*
 Template table containing with elements for automatic tables 
 */
CREATE TEMP TABLE automatic_templ (
    import_source VARCHAR(500) NOT NULL CHECK (import_source <> ''),
    import_time TIMESTAMP NOT NULL
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

-- Template to use for the actual tables. This makes sure their schemas
-- are defined in the same way.
CREATE TEMP TABLE organisation_templ (
    -- The name of the organisation.
    -- In the ripe db there are names identical for more than one
    -- organisation, so we can not make this unique.
    name VARCHAR(500) NOT NULL,

    -- The sector the organisation belongs to.
    sector_id INTEGER,

    -- Comments about the organisation
    comment TEXT NOT NULL DEFAULT '',

    -- The org: nic handle in the RIPE DB, if available
    ripe_org_hdl VARCHAR(100) NOT NULL DEFAULT '',

    -- The Trusted Introducer (TI) handle or URL: for example
    -- https://www.trusted-introducer.org/directory/teams/certat.html
    ti_handle VARCHAR(500) NOT NULL DEFAULT '',

    -- The FIRST.org handle or URL: for example
    -- https://api.first.org/data/v1/teams?q=aconet-cert
    first_handle VARCHAR(500) NOT NULL DEFAULT ''
);


CREATE TABLE organisation (
    id SERIAL PRIMARY KEY,
    LIKE organisation_templ INCLUDING ALL,

    FOREIGN KEY (sector_id) REFERENCES sector(id)
);


CREATE TABLE organisation_automatic (
    id SERIAL PRIMARY KEY,
    LIKE organisation_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL,

    FOREIGN KEY (sector_id) REFERENCES sector(id)
);


CREATE TABLE organisation_annotation (
    id SERIAL PRIMARY KEY,
    organisation_id INTEGER NOT NULL,
    annotation JSON NOT NULL,

    FOREIGN KEY (organisation_id) REFERENCES organisation(id)
);

CREATE INDEX organisation_annotation_organisation_idx
          ON organisation_annotation (organisation_id);



CREATE TEMP TABLE contact_templ (
    firstname VARCHAR (500) NOT NULL DEFAULT '',
    lastname  VARCHAR (500) NOT NULL DEFAULT '',
    tel       VARCHAR (500) NOT NULL DEFAULT '',

    -- The full fingerprint of the OpenPGP pubkey of the contact as GnuPG
    -- would accept it to specify a user ID.
    -- (This avoids ambiguities in case that there are duplicated key IDs.)
    openpgp_fpr VARCHAR(128) NOT NULL DEFAULT '',

    -- the email-address of the contact
    email VARCHAR(100) NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    LIKE contact_templ INCLUDING ALL
);


CREATE TABLE contact_automatic (
    id SERIAL PRIMARY KEY,
    LIKE contact_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL
);


-- Roles serve as an m-n relationship between organisations and contacts
CREATE TEMP TABLE role_templ (
    -- free text for right now. We assume the regular tags from the
    -- RIPE DB such as "tech-c" or "abuse-c"
    -- possible values: "abuse-c", "billing-c" , "admin-c"
    role_type VARCHAR (500) NOT NULL default 'abuse-c',
    is_primary_contact BOOLEAN NOT NULL DEFAULT FALSE,

    organisation_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL
);


CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    LIKE role_templ INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation(id),
    FOREIGN KEY (contact_id) REFERENCES contact(id)
);

CREATE INDEX role_organisation_id_idx
          ON role (organisation_id);
CREATE INDEX role_contact_id_idx
          ON role (contact_id);

CREATE TABLE role_automatic (
    id SERIAL PRIMARY KEY,
    LIKE role_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic(id),
    FOREIGN KEY (contact_id) REFERENCES contact_automatic(id)
);

CREATE INDEX role_automatic_organisation_id_idx
          ON role_automatic (organisation_id);
CREATE INDEX role_automatic_contact_id_idx
          ON role_automatic (contact_id);


/*
  Network related tables, such as:
  AS, IP-Ranges, FQDN
*/

-- An autonomous system
CREATE TEMP TABLE autonomous_system_templ (
    -- The autonomous system number
    number BIGINT,

    -- RIPE handle (see
    -- https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/ripe-database-structure/3-1-list-of-primary-objects)
    -- and:
    -- https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-1-description-of-the-aut-num-object
    ripe_aut_num VARCHAR(100) NOT NULL DEFAULT '',

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE autonomous_system (
    id SERIAL PRIMARY KEY,
    LIKE autonomous_system_templ INCLUDING ALL
);

CREATE TABLE autonomous_system_automatic (
    id SERIAL PRIMARY KEY,
    LIKE autonomous_system_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL
);


CREATE TABLE autonomous_system_annotation (
    id SERIAL PRIMARY KEY,
    asn_id BIGINT NOT NULL,
    annotation JSON NOT NULL,

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (id)
);

CREATE INDEX autonomous_system_annotation_asn_id
          ON autonomous_system_annotation (asn_id);



-- A network
-- See also: https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-4-description-of-the-inetnum-object
CREATE TEMP TABLE network_templ (
    -- Network address as CIDR.
    address cidr UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE network (
    id SERIAL PRIMARY KEY,
    LIKE network_templ INCLUDING ALL
);

CREATE TABLE network_automatic (
    id SERIAL PRIMARY KEY,
    LIKE network_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL
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



-- Annotations for networks
CREATE TABLE network_annotation (
    id SERIAL PRIMARY KEY,
    network_id INTEGER NOT NULL,
    annotation JSON NOT NULL,

    FOREIGN KEY (network_id) REFERENCES network(id)
);

CREATE INDEX network_annotation_network_idx
          ON network_annotation (network_id);




-- A fully qualified domain name
CREATE TEMP TABLE fqdn_templ (
    -- The fully qualified domain name
    fqdn TEXT UNIQUE NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE fqdn (
    id SERIAL PRIMARY KEY,
    LIKE fqdn_templ INCLUDING ALL
);


CREATE TABLE fqdn_automatic (
    id SERIAL PRIMARY KEY,
    LIKE fqdn_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL
);


CREATE TABLE fqdn_annotation (
    id SERIAL PRIMARY KEY,
    fqdn_id INTEGER NOT NULL,
    annotation JSON NOT NULL,

    FOREIGN KEY (fqdn_id) REFERENCES fqdn(id)
);

CREATE INDEX fqdn_annotation_fqdn_idx
          ON fqdn_annotation (fqdn_id);



-- Information about national CERTs

-- national_cert relates a country code to the organisation considered
-- the national CERT for that country.
CREATE TEMP TABLE national_cert_templ (
    -- The country code for the CERT
    country_code CHARACTER(2) NOT NULL,

    -- The ID of the organisation representing the CERT
    organisation_id INTEGER NOT NULL,

    comment TEXT NOT NULL DEFAULT ''
);


CREATE TABLE national_cert (
    id SERIAL PRIMARY KEY,
    LIKE national_cert_templ INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation (id)
);

CREATE INDEX national_cert_country_code_idx
          ON national_cert (country_code);


-- Like national_cert but for automatically maintained data.
CREATE TABLE national_cert_automatic (
    id SERIAL PRIMARY KEY,
    LIKE national_cert_templ INCLUDING ALL,
    LIKE automatic_templ INCLUDING ALL,

    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id)
);

CREATE INDEX national_cert_automatic_country_code_idx
          ON national_cert_automatic (country_code);


/*
 Relations A_to_B
 Some of them (contact_to_X) carry an additional column TTL
 See also https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/ripe-database-structure/3-1-list-of-primary-objects
*/
CREATE TABLE organisation_to_asn (
    organisation_id INTEGER,
    asn_id BIGINT,

    PRIMARY KEY (organisation_id, asn_id),

    FOREIGN KEY (asn_id) REFERENCES autonomous_system (id),
    FOREIGN KEY (organisation_id) REFERENCES organisation (id)
);


CREATE TABLE organisation_to_asn_automatic (
    LIKE automatic_templ INCLUDING ALL,
    LIKE organisation_to_asn INCLUDING ALL,

    FOREIGN KEY (asn_id) REFERENCES autonomous_system_automatic (id),
    FOREIGN KEY (organisation_id) REFERENCES organisation_automatic (id)
);


CREATE TABLE organisation_to_network (
    organisation_id INTEGER,
    net_id INTEGER,

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




COMMIT;
