# Indices for the asn column on the organisation_to_asn tables

## upgrade
```sql
CREATE INDEX organisation_to_asn_asn_idx
    ON organisation_to_asn (asn);
CREATE INDEX organisation_to_asn_automatic_asn_idx
    ON organisation_to_asn_automatic (asn);
```

## downgrade
```sql
DROP INDEX organisation_to_asn_asn_idx;
DROP INDEX organisation_to_asn_automatic_asn_idx;
```


# Add FQDN index again

This index was implicitly removed by the removal of the UNIQUE
constraint on fqdn (fqdn). The analogous index on network (address) is
not needed currently and therefore it's not a problem that it was
removed together the UNIQUE constraint.


## upgrade
```sql
CREATE INDEX fqdn_fqdn_idx ON fqdn (fqdn);
```


## downgrade
```sql
DROP INDEX fqdn_fqdn_idx;
```


# Enabling multiple entries for fqdn and network

## upgrade

```sql
ALTER TABLE fqdn DROP CONSTRAINT fqdn_fqdn_key;
ALTER TABLE network DROP CONSTRAINT network_address_key;
```

## downgrade
```sql
ALTER TABLE fqdn ADD CONSTRAINT fqdn_fqdn_key UNIQUE (fqdn);
ALTER TABLE network ADD  CONSTRAINT network_address_key UNIQUE (address);
```


# Intevation/intelmq/issues/17 (certbund-contact: renaming pgp_key_id)

## upgrade
```sql
-- you may need to close other connections/cursors to the db before
ALTER TABLE contact RENAME COLUMN pgp_key_id TO openpgp_fpr;
ALTER TABLE contact_automatic RENAME COLUMN pgp_key_id TO openpgp_fpr;
```

## downgrade
```sql
-- you may need to close other connections/cursors to the db before
ALTER TABLE contact RENAME COLUMN openpgp_fpr TO pgp_key_id;
ALTER TABLE contact_automatic RENAME COLUMN openpgp_fpr TO pgp_key_id;
```
