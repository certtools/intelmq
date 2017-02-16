# Intevation/intelmq/issues/17 (certbund-contact: renaming pgp_key_id)

## forward
```sql
ALTER TABLE contact RENAME COLUMN pgp_key_id TO openpgp_fpr;
```

## backward
```sql
ALTER TABLE contact RENAME COLUMN openpgp_fpr TO pgp_key_id;
```
