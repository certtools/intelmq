Request Tracker collector
=========================

You need the rt-library from nic.cz, available via [pypi](https://pypi.python.org/pypi/rt):

    pip install rt

Version 1.0.9 is required, as older version have bugs.

The bot searches for tickets matching the criteria in `search_*`, all of these
will be inspected. Then, all attachments of the ticket are iterated and the
filename matched against the regex. If none of them applies, the content of the
first history item is matched against the URL-regex.

Attachments can be optionally unzipped, remote files are downloaded with the
`http_*` settings applied (see `defaults.conf`).

Optionally, tickets can be taken by the used user and/or the status can be
changed (leave empty for unmodified). One of the both should be used, otherwise
the search will find the ticket every time.

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

