FROM debian:buster

ENV LANG C.UTF-8
WORKDIR /opt/intelmq

COPY . /opt/intelmq

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-nose \
    python3-yaml \
    python3-cerberus \
    python3-requests-mock \
    python3-dev \
    python3-setuptools \
    python3-pip

RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -e .
RUN useradd -d /opt/intelmq -U -s /bin/bash intelmq
RUN intelmqsetup
RUN chown -R intelmq:intelmq /opt/intelmq

RUN chmod +x entrypoint.sh

USER intelmq

ENTRYPOINT [ "./.docker/entrypoint.sh" ]
