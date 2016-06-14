Request Tracker collector
=========================

A fork of python-rt is needed which fixes relevant bugs:
https://github.com/wtsi-hgi/python-rt.git

The bot searches for tickets matching the criteria in `search_*`, all of these
will be inspected. Then, all attachments of the ticket are iterated and the
filename matched against the regex. If none of them applies, the content of the
first history item is matched against the URL-regex.

Attachments can be optionally unzipped, remote files are downloaded with the
`http_*` settings applied (see `defaults.conf`).

Optionally, tickets can be taken by the used user, which is recommended
(otherwise the search may find the ticket again).

    "request-tracker-collector": {
        "attachment_regex": "\\.csv\\.zip$",
        "feed": "Request Tracker",
        "password": "intelmq",
        "search_queue": "Incident Reports",
        "search_subject_like": "Report",
        "search_owner": "nobody",
        "search_status": "new",
        "take_ticket": true,
        "rate_limit": 3600,
        "url_regex": "https://dl.shadowserver.org/[a-zA-Z0-9?_-]*",
        "uri": "http://localhost/rt/REST/1.0",
        "user": "intelmq",
        "unzip_attachment": true
    },

