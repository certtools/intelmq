-- SPDX-FileCopyrightText: 2021 Sebastian Wagner
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

-- Create the table holding only the "raw" values:

CREATE TABLE public.raws (
    event_id bigint,
    raw text
);

ALTER TABLE
    public.raws OWNER TO intelmq;

CREATE INDEX idx_raws_event_id ON public.raws USING btree (event_id);

ALTER TABLE
    ONLY public.raws
ADD
    CONSTRAINT raws_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE;

-- Create the v_events view which joins the tables "events" and "raws"

CREATE VIEW public.v_events AS
    SELECT events.id,
        events."classification.identifier",
        events."classification.taxonomy",
        events."classification.type",
        events."comment",
        events."destination.abuse_contact"
        events."destination.account"
        events."destination.allocated"
        events."destination.asn"
        events."destination.as_name"
        events."destination.domain_suffix",
        events."destination.fqdn"
        events."destination.geolocation.cc",
        events."destination.geolocation.city"
        events."destination.geolocation.country"
        events."destination.geolocation.latitude"
        events."destination.geolocation.longitude"
        events."destination.geolocation.region"
        events."destination.geolocation.state"
        events."destination.ip"
        events."destination.local_hostname"
        events."destination.local_ip"
        events."destination.network"
        events."destination.port"
        events."destination.registry"
        events."destination.reverse_dns"
        events."destination.tor_node"
        events."destination.url"
        events."destination.urlpath",
        events."event_description.target",
        events."event_description.text",
        events."event_description.url",
        events."event_hash",
        events."extra",
        events."feed.accuracy",
        events."feed.code",
        events."feed.documentation",
        events."feed.name",
        events."feed.provider",
        events."feed.url",
        events."malware.hash",
        events."malware.hash.md5",
        events."malware.hash.sha1",
        events."malware.hash.sha256",
        events."malware.name",
        events."malware.version",
        events."misp.attribute_uuid",
        events."misp.event_uuid",
        events."protocol.application",
        events."protocol.transport",
        events."rtir_id",
        events."screenshot_url",
        events."source.abuse_contact",
        events."source.account",
        events."source.allocated",
        events."source.asn",
        events."source.as_name",
        events."source.domain_suffix",
        events."source.fqdn",
        events."source.geolocation.cc",
        events."source.geolocation.city",
        events."source.geolocation.country",
        events."source.geolocation.cymru_cc",
        events."source.geolocation.geoip_cc",
        events."source.geolocation.latitude",
        events."source.geolocation.longitude",
        events."source.geolocation.region",
        events."source.geolocation.state",
        events."source.ip",
        events."source.local_hostname",
        events."source.local_ip",
        events."source.network",
        events."source.port",
        events."source.registry",
        events."source.reverse_dns",
        events."source.tor_node",
        events."source.url",
        events."source.urlpath",
        events."status",
        events."time.observation",
        events."time.source",
        events."tlp"
        raws."event_id",
        raws."raw",
    FROM (
        public.events
        JOIN public.raws ON ((events.id = raws.event_id)));

-- Establish the INSERT trigger for the events table, splitting the data into events and raws

CREATE FUNCTION public.process_v_events_insert()
    RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE event_id integer;

    BEGIN
        -- add all data except raw to events
        INSERT INTO
            events (
                "classification.identifier",
                "classification.taxonomy",
                "classification.type",
                "comment",
                "destination.abuse_contact",
                "destination.account",
                "destination.allocated",
                "destination.asn",
                "destination.as_name",
                "destination.domain_suffix",
                "destination.fqdn",
                "destination.geolocation.cc",
                "destination.geolocation.city",
                "destination.geolocation.country",
                "destination.geolocation.latitude",
                "destination.geolocation.longitude",
                "destination.geolocation.region",
                "destination.geolocation.state",
                "destination.ip",
                "destination.local_hostname",
                "destination.local_ip",
                "destination.network",
                "destination.port",
                "destination.registry",
                "destination.reverse_dns",
                "destination.tor_node",
                "destination.url",
                "destination.urlpath",
                "event_description.target",
                "event_description.text",
                "event_description.url",
                "event_hash",
                "extra",
                "feed.accuracy",
                "feed.code",
                "feed.documentation",
                "feed.name",
                "feed.provider",
                "feed.url",
                "malware.hash",
                "malware.hash.md5",
                "malware.hash.sha1",
                "malware.name",
                "malware.version",
                "misp.attribute_uuid",
                "misp.event_uuid",
                "protocol.application",
                "protocol.transport",
                "rtir_id",
                "screenshot_url",
                "source.abuse_contact",
                "source.account",
                "source.allocated",
                "source.asn",
                "source.as_name",
                "source.domain_suffix",
                "source.fqdn",
                "source.geolocation.cc",
                "source.geolocation.city",
                "source.geolocation.country",
                "source.geolocation.cymru_cc",
                "source.geolocation.geoip_cc",
                "source.geolocation.latitude",
                "source.geolocation.longitude",
                "source.geolocation.region",
                "source.geolocation.state",
                "source.ip",
                "source.local_hostname",
                "source.local_ip",
                "source.network",
                "source.port",
                "source.registry",
                "source.reverse_dns",
                "source.tor_node",
                "source.url",
                "source.urlpath",
                "status",
                "time.observation",
                "time.source",
                "tlp"
            )
        VALUES
            (
                NEW."classification.identifier",
                NEW."classification.taxonomy",
                NEW."classification.type",
                NEW."comment",
                NEW."destination.abuse_contact",
                NEW."destination.account",
                NEW."destination.allocated",
                NEW."destination.asn",
                NEW."destination.as_name",
                NEW."destination.domain_suffix",
                NEW."destination.fqdn",
                NEW."destination.geolocation.cc",
                NEW."destination.geolocation.city",
                NEW."destination.geolocation.country",
                NEW."destination.geolocation.latitude",
                NEW."destination.geolocation.longitude",
                NEW."destination.geolocation.region",
                NEW."destination.geolocation.state",
                NEW."destination.ip",
                NEW."destination.local_hostname",
                NEW."destination.local_ip",
                NEW."destination.network",
                NEW."destination.port",
                NEW."destination.registry",
                NEW."destination.reverse_dns",
                NEW."destination.tor_node",
                NEW."destination.url",
                NEW."destination.urlpath",
                NEW."event_description.target",
                NEW."event_description.text",
                NEW."event_description.url",
                NEW."event_hash",
                NEW."extra",
                NEW."feed.accuracy",
                NEW."feed.code",
                NEW."feed.documentation",
                NEW."feed.name",
                NEW."feed.provider",
                NEW."feed.url",
                NEW."malware.hash",
                NEW."malware.hash.md5",
                NEW."malware.hash.sha1",
                NEW."malware.name",
                NEW."malware.version",
                NEW."misp.attribute_uuid",
                NEW."misp.event_uuid",
                NEW."protocol.application",
                NEW."protocol.transport",
                NEW."rtir_id",
                NEW."screenshot_url",
                NEW."source.abuse_contact",
                NEW."source.account",
                NEW."source.allocated",
                NEW."source.asn",
                NEW."source.as_name",
                NEW."source.domain_suffix",
                NEW."source.fqdn",
                NEW."source.geolocation.cc",
                NEW."source.geolocation.city",
                NEW."source.geolocation.country",
                NEW."source.geolocation.cymru_cc",
                NEW."source.geolocation.geoip_cc",
                NEW."source.geolocation.latitude",
                NEW."source.geolocation.longitude",
                NEW."source.geolocation.region",
                NEW."source.geolocation.state",
                NEW."source.ip",
                NEW."source.local_hostname",
                NEW."source.local_ip",
                NEW."source.network",
                NEW."source.port",
                NEW."source.registry",
                NEW."source.reverse_dns",
                NEW."source.tor_node",
                NEW."source.url",
                NEW."source.urlpath",
                NEW."status",
                NEW."time.observation",
                NEW."time.source",
                NEW."tlp"
            ) RETURNING id INTO event_id;

        -- add the raw value to raws, link with the event_id
        INSERT INTO
            raws ("event_id", "raw")
        VALUES
            (event_id, NEW.raw);

        RETURN NEW;

    END;
$$;

CREATE TRIGGER tr_events
    INSTEAD OF INSERT
    ON public.v_events
    FOR EACH ROW
    EXECUTE FUNCTION public.process_v_events_insert();
