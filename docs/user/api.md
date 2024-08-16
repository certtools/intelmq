<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Using IntelMQ API

!!! bug
    This section of the documentation is currently incomplete and will be added later.

## Usage from programs


The IntelMQ API can also be used from programs, not just browsers. To do
so, first send a POST-Request with JSON-formatted data to
<http://localhost/intelmq/v1/api/login/>

```json
{
    "username": "$your_username",
    "password": "$your_password"
}
```

With valid credentials, the JSON-formatted response contains the
`login_token`. This token can be used like an API key in the
Authorization header for the next API calls:

```bash
Authorization: $login_token
```

Here is a full example using **curl**:

1. Authentication step:
   ```bash
   curl --location --request POST "http://localhost/intelmq/v1/api/login/" \
        --header "Content-Type: application/x-www-form-urlencoded" \
        --data-urlencode "username=$username"\
        --data-urlencode "password=$password"
   ```
   ```json
   {"login_token":"68b329da9893e34099c7d8ad5cb9c940","username":"$username"}
   ```

2. Using the login token to fetch data:
   ```bash
   curl --location "http://localhost/intelmq/v1/api/version" \
        --header "Authorization: 68b329da9893e34099c7d8ad5cb9c940"
   ```
   ```json
   {"intelmq":"3.0.0rc1","intelmq-manager":"2.3.1"}
   ```

The same approach also works for *Ansible*, as you can see here:

1.  <https://github.com/schacht-certat/intelmq-vagrant/blob/7082719609c0aafc9324942a8775cf2f8813703d/ansible/tasks/api/00_registerauth.yml#L1-L9>
2.  <https://github.com/schacht-certat/intelmq-vagrant/blob/7082719609c0aafc9324942a8775cf2f8813703d/ansible/tasks/api/02_queuestatus.yml#L1-L5>