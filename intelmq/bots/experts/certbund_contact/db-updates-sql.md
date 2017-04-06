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
