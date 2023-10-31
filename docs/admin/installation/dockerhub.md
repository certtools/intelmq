<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Installation from DockerHub

This guide provides instruction on how to install IntelMQ and it's components using Docker.

!!! warning
    Docker installation is currently in Beta state and things might break. Consider this if you plan to use IntelMQ as a production level system.

!!! warning
    Currently you can't manage your botnet via `intelmqctl` command line tool. You need to use [IntelMQ-Manager](https://github.com/certtools/intelmq-manager) currently!

The latest IntelMQ image is hosted on [Docker Hub](https://hub.docker.com/r/certat/intelmq-full) and the image build instructions are in our [intelmq-docker repository](https://github.com/certat/intelmq-docker).

Follow [Docker Install](https://docs.docker.com/engine/install/) and
[Docker-Compose Install](https://docs.docker.com/compose/install/)
instructions.

Before you start using docker-compose or any docker related tools, make
sure docker is running:

```bash
# To start the docker daemon
systemctl start docker.service
# To enable the docker daemon for the future
systemctl enable docker.service
```

## Docker with docker-compose

Now we can download IntelMQ and start the containers. Navigate to your
preferred installation directory and run the following commands:

```bash
git clone https://github.com/certat/intelmq-docker.git --recursive
cd intelmq-docker
sudo docker-compose pull
sudo docker-compose up
```

Your installation should be successful now. You're now able to visit
`http://127.0.0.1:1337/` to access the intelmq-manager. You have to
login with the username `intelmq` and the password `intelmq`, if you
want to change the username or password, you can do this by adding the
environment variables `INTELMQ_API_USER` for the username and
`INTELMQ_API_PASS` for the password.


!!! note
    If you get an **Permission denied** error, you should run `chown -R $USER:$USER example_config`



## Docker without docker-compose

If not already installed, please install
[Docker](https://docs.docker.com/get-docker/).

Navigate to your preferred installation directory and run
`git clone https://github.com/certat/intelmq-docker.git --recursive`.

You need to prepare some volumes & configs. Edit the left-side after -v,
to change paths.

Change `redis_host` to a running redis-instance. Docker will resolve it
automatically. All containers are connected using [Docker
Networks](https://docs.docker.com/engine/tutorials/networkingcontainers/).

In order to work with your current infrastructure, you need to specify
some environment variables

```bash
sudo docker pull redis:latest

sudo docker pull certat/intelmq-full:latest

sudo docker pull certat/intelmq-nginx:latest

sudo docker network create intelmq-internal

sudo docker run -v ~/intelmq/example_config/redis/redis.conf:/redis.conf \
                --network intelmq-internal \
                --name redis \
                redis:latest

sudo docker run --network intelmq-internal \
                --name nginx \
                certat/intelmq-nginx:latest

sudo docker run -e INTELMQ_IS_DOCKER="true" \
                -e INTELMQ_SOURCE_PIPELINE_BROKER: "redis" \
                -e INTELMQ_PIPELINE_BROKER: "redis" \
                -e INTELMQ_DESTIONATION_PIPELINE_BROKER: "redis" \
                -e INTELMQ_PIPELINE_HOST: redis \
                -e INTELMQ_SOURCE_PIPELINE_HOST: redis \
                -e INTELMQ_DESTINATION_PIPELINE_HOST: redis \
                -e INTELMQ_REDIS_CACHE_HOST: redis \
                -v $(pwd)/example_config/intelmq/etc/:/etc/intelmq/etc/ \
                -v $(pwd)/example_config/intelmq-api/config.json:/etc/intelmq/api-config.json \
                -v $(pwd)/intelmq_logs:/etc/intelmq/var/log \
                -v $(pwd)/intelmq_output:/etc/intelmq/var/lib/bots \
                -v ~/intelmq/lib:/etc/intelmq/var/lib \
                --network intelmq-internal \
                --name intelmq \
                certat/intelmq-full:latest
```

If you want to use another username and password for the intelmq-manager
/ api login, additionally add two new environment variables.

```bash
-e INTELMQ_API_USER: "your username"
-e INTELMQ_API_PASS: "your password"
```
