`intelmqcli`: Command Line Interface
====================================

The cli tool fetches unhandled events from the events database and creates tickets in an RTIR instance to notify the abuse contacts of the AS.

Start the programm to see an overview of open events:

```bash
intelmq ~ $ ./bin/intelmqcli
====================================================================================================
 id n°  ASNs              contacts                    types
  0  30 16305, 1901, 8447 abuse@a1telekom.at          ids alert
  1   1 62239             abuse@bis.at                brute-force
  2   1 8559              abuse@bnet.at               ids alert
  3  16 43449             abuse@dimline.org           brute-force, ids alert
  4   1 35492             abuse@funkfeuer.at          ids alert
  5   2 5385              abuse@TELE.NET              ids alert
  6   1 6830              abuse@upc.at                ids alert
  7   4 8437              abuse@uta.at,abuse@tele2.at ids alert
  8   1 197999            office@em-it.at             ids alert
57 incidents for 9 contacts.
detailed view by id, (a)utomatic sending, (q)uit?
```

We want to see some details for one of the entries, e.g. for dimline. so we answer `3`:

```bash
detailed view by id, (a)utomatic sending, (q)uit? 3
====================================================================================================
To: abuse@dimline.org
Subject: 2015-09-21: 16 incidents for your AS

message text

classification.type,feed.name,id,source.asn,source.ip,source.reverse_dns,time.source
ids alert,BlockList.de,35521934,43449,91.194.254.146,,
ids alert,BlockList.de,35521930,43449,91.194.254.142,,
ids alert,BlockList.de,35521931,43449,91.194.254.143,,
ids alert,BlockList.de,35521932,43449,91.194.254.144,,
ids alert,BlockList.de,35521933,43449,91.194.254.145,,
ids alert,BlockList.de,37088568,43449,91.194.254.142,hosted-by.dimline.org.,
ids alert,BlockList.de,37088569,43449,91.194.254.143,hosted-by.dimline.org.,
ids alert,BlockList.de,37088570,43449,91.194.254.144,hosted-by.dimline.org.,
ids alert,BlockList.de,37088571,43449,91.194.254.146,hosted-by.dimline.org.,
brute-force,Dragon Research Group,37774545,43449,91.194.254.144,hosted-by.dimline.org.,2015-09-14T00:00:00+00
brute-force,Dragon Research Group,37774546,43449,91.194.254.145,hosted-by.dimline.org.,2015-09-13T00:00:00+00
brute-force,Dragon Research Group,37774547,43449,91.194.254.142,hosted-by.dimline.org.,2015-09-14T00:00:00+00
brute-force,Dragon Research Group,37774548,43449,91.194.254.143,hosted-by.dimline.org.,2015-09-14T00:00:00+00
brute-force,Dragon Research Group,37978313,43449,91.194.254.144,hosted-by.dimline.org.,2015-09-14T00:00:00+00
brute-force,Dragon Research Group,37978314,43449,91.194.254.142,hosted-by.dimline.org.,2015-09-14T00:00:00+00
brute-force,Dragon Research Group,37978315,43449,91.194.254.143,hosted-by.dimline.org.,2015-09-14T00:00:00+00

----------------------------------------------------------------------------------------------------
(b)ack, (s)end, show (t)able, change (r)equestor or (q)uit?
```

The data is hard to read in csv format, so we press `t`:

```bash
(b)ack, (s)end, show (t)able, change (r)equestor or (q)uit? t
====================================================================================================
To: abuse@dimline.org
Subject: 2015-09-21: 16 incidents for your AS

TODO: text

 +---------------------+-----------------------+----------+------------+----------------+------------------------+------------------------+
| classification.type |       feed.name       |    id    | source.asn |   source.ip    |   source.reverse_dns   |      time.source       |
+---------------------+-----------------------+----------+------------+----------------+------------------------+------------------------+
|      ids alert      |      BlockList.de     | 35521934 |   43449    | 91.194.254.146 |                        |                        |
|      ids alert      |      BlockList.de     | 35521930 |   43449    | 91.194.254.142 |                        |                        |
|      ids alert      |      BlockList.de     | 35521931 |   43449    | 91.194.254.143 |                        |                        |
|      ids alert      |      BlockList.de     | 35521932 |   43449    | 91.194.254.144 |                        |                        |
|      ids alert      |      BlockList.de     | 35521933 |   43449    | 91.194.254.145 |                        |                        |
|      ids alert      |      BlockList.de     | 37088568 |   43449    | 91.194.254.142 | hosted-by.dimline.org. |                        |
|      ids alert      |      BlockList.de     | 37088569 |   43449    | 91.194.254.143 | hosted-by.dimline.org. |                        |
|      ids alert      |      BlockList.de     | 37088570 |   43449    | 91.194.254.144 | hosted-by.dimline.org. |                        |
|      ids alert      |      BlockList.de     | 37088571 |   43449    | 91.194.254.146 | hosted-by.dimline.org. |                        |
|     brute-force     | Dragon Research Group | 37774545 |   43449    | 91.194.254.144 | hosted-by.dimline.org. | 2015-09-14T00:00:00+00 |
|     brute-force     | Dragon Research Group | 37774546 |   43449    | 91.194.254.145 | hosted-by.dimline.org. | 2015-09-13T00:00:00+00 |
|     brute-force     | Dragon Research Group | 37774547 |   43449    | 91.194.254.142 | hosted-by.dimline.org. | 2015-09-14T00:00:00+00 |
|     brute-force     | Dragon Research Group | 37774548 |   43449    | 91.194.254.143 | hosted-by.dimline.org. | 2015-09-14T00:00:00+00 |
|     brute-force     | Dragon Research Group | 37978313 |   43449    | 91.194.254.144 | hosted-by.dimline.org. | 2015-09-14T00:00:00+00 |
|     brute-force     | Dragon Research Group | 37978314 |   43449    | 91.194.254.142 | hosted-by.dimline.org. | 2015-09-14T00:00:00+00 |
|     brute-force     | Dragon Research Group | 37978315 |   43449    | 91.194.254.143 | hosted-by.dimline.org. | 2015-09-14T00:00:00+00 |
+---------------------+-----------------------+----------+------------+----------------+------------------------+------------------------+
----------------------------------------------------------------------------------------------------
(b)ack, (s)end, show (t)able, change (r)equestor or (q)uit?
```

Much easier to read. This mail will be sent in csv format anyway.

Change the requestor, the recipient of the report, by pressing `r`:


```bash
(b)ack, (s)end, show (t)able, change (r)equestor or (q)uit? r
New requestor address: null@localhost.invalid
====================================================================================================
To: null@localhost.invalid
```

Now we are ready to create the tickets and send the mail out:

```bash
(b)ack, (s)end, show (t)able, change (r)equestor or (q)uit? s
intelmqcli: Created Incident Report 113.
intelmqcli: Created Incident 114.
intelmqcli: Created Investigation 115.
```
The program asks if the recipient should be saved to the database. an existing record will be updated or a new one will be added:
```bash
Save recipient 'null@localhost' for ASNs 1206? [Y/n]
```
Then we come back to the start screen, with fresh data from the database:
```bash
====================================================================================================
 id n°  ASNs              contacts                    types
  0  30 16305, 1901, 8447 abuse@a1telekom.at          ids alert
  1   1 62239             abuse@bis.at                brute-force
  2   1 8559              abuse@bnet.at               ids alert
  3  16 43449             abuse@dimline.org           brute-force, ids alert
  4   1 35492             abuse@funkfeuer.at          ids alert
  5   2 5385              abuse@TELE.NET              ids alert
  6   1 6830              abuse@upc.at                ids alert
  7   4 8437              abuse@uta.at,abuse@tele2.at ids alert
  8   1 197999            office@em-it.at             ids alert
  9   1 135435                                        test
58 incidents for 10 contacts.
```
