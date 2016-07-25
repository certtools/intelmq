Request Tracker collector
=========================

You need the rt-library from nic.cz, available via [pypi](https://pypi.python.org/pypi/rt):

    pip install rt

Version 1.0.9 is required, as older version have bugs.

This rt bot will connect to RT and inspect the given `search_queue` for tickets matching all criteria in `search_*`, 
Any matches will be inspected. For each match, all (RT-) attachments of the matching RT tickets are iterated over and within this loop, the first matching filename in the attachment is processed.
If none of the filename matches apply, the contents of the first (RT-) "history" item is matched against the URL-regex.

Attachments can be optionally unzipped, remote files are downloaded with the `http_*` settings applied (see `defaults.conf`).

Optionally, the RT bot can "take" RT tickets (i.e. the `user` is assigned this ticket now) and/or the status can be changed (leave `set_status` empty in case you don't want to change the status). Please note however that you **MUST** do one of the following: either "take" the ticket  or set the status (`set_status`). Otherwise, the search will find the ticket every time and we will have generated an endless loop.


    "request-tracker-collector": {
        "attachment_regex": "\\.csv\\.zip$",
        "feed": "Request Tracker",
        "password": "intelmq",
        "search_queue": "Incident Reports",
        "search_subject_like": "Report",
        "search_owner": "nobody",
        "search_status": "new",
        "set_status": "open",
        "take_ticket": true,
        "rate_limit": 3600,
        "url_regex": "https://dl.shadowserver.org/[a-zA-Z0-9?_-]*",
        "uri": "http://localhost/rt/REST/1.0",
        "user": "intelmq",
        "unzip_attachment": true
    },

