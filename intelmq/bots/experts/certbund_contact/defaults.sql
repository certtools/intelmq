BEGIN;

INSERT INTO format (name) VALUES ('csv');
INSERT INTO format (name) VALUES ('feed_specific');


-- classification_type values taken from the ClassificationType class in
-- intelmq/lib/harmonization.py
INSERT INTO classification_type (name) VALUES
    ('spam'),
    ('malware'),
    ('botnet drone'),
    ('ransomware'),
    ('malware configuration'),
    ('c&c'),
    ('scanner'),
    ('exploit'),
    ('brute-force'),
    ('ids alert'),
    ('defacement'),
    ('compromised'),
    ('backdoor'),
    ('ddos'),
    ('dropzone'),
    ('phishing'),
    ('vulnerable service'),
    ('blacklist'),
    ('other'),
    ('unknown');


INSERT INTO classification_identifier (name) VALUES
    ('openchargen'),
    ('opendns'),
    ('openelasticsearch'),
    ('openipmi'),
    ('openmdns'),
    ('openmemcached'),
    ('openmongodb'),
    ('openmssql'),
    ('opennetbios'),
    ('openntp'),
    ('openportmapper'),
    ('openqotd'),
    ('openredis'),
    ('openssdp'),
    ('opentftp'),
    ('snmp');


COMMIT;
