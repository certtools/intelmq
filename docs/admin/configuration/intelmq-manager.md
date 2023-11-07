<!-- comment
   SPDX-FileCopyrightText: 2015 Aaron Kaplan <aaron@lo-res.org>, 2015-2021 Sebastian Wagner, 2020-2021 Birger Schacht, 2023 Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Configuring IntelMQ Manager

In the file `/usr/share/intelmq-manager/html/js/vars.js` set `ROOT` to the URL of your `intelmq-api` installation - by
default that's on the same host as `intelmq-manager`.

## Configuration Paths

The IntelMQ Manager queries the configuration file paths and directory names from `intelmqctl` and therefore any global
environment variables
(if set) are effective in the Manager too. The interface for this query is `intelmqctl debug --get-paths`, the result is
also shown in the
`/about.html` page of your IntelMQ Manager installation.

## CSP Headers

It is recommended to set these two headers for all requests:

```
Content-Security-Policy: script-src 'self'
X-Content-Security-Policy: script-src 'self'
```

## Security considerations

Never ever run intelmq-manager on a public webserver without SSL and proper authentication!

The way the current version is written, anyone can send a POST request and change intelmq's configuration files via
sending HTTP POST requests. Intelmq-manager will reject non JSON data but nevertheless, we don't want anyone to be able
to reconfigure an intelmq installation.

Therefore you will need authentication and SSL. Authentication can be handled by the `intelmq-api`. Please refer to its
documentation on how to enable authentication and setup accounts.

Never ever allow unencrypted, unauthenticated access to IntelMQ Manager!

### Docker: Security headers

If you run our docker image in production, we recommend you to set security headers. You can do this by creating a new
file called
`example_config/nginx/security.conf` in the cloned `intelmq-docker`
repository.

Write the following inside the configuration file, and change the
`http(s)://<your-domain>` to your domain name.

```bash
server_tokens off; # turn off server_token, instead of nginx/13.2 now it will only show nginx
add_header X-Frame-Options SAMEORIGIN; # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
add_header X-Content-Type-Options nosniff; # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
add_header X-XSS-Protection "1; mode=block"; # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
add_header Content-Security-Policy "script-src 'self' 'unsafe-inline' http(s)://<your-domain>; frame-src 'self' http(s)://<your-domain>; object-src 'self' http(s)://<your-domain>"; # https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
```

After you created the file, edit the `docker-compose.yml` and mount it to the `nginx` with

```yaml
volumes:
  - ./example_config/nginx/security.conf:/etc/nginx/conf.d/security.conf
```

**IMPORTANT** Mount the exact name & not the directory, because otherwise you would overwrite the whole directory and
the other files would be gone inside the container.
