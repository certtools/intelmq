# Request Tracker output bot

Bot creates tickets in Request Tracker, puts attributes into the ticket body. Bot can follow the workflow of the RTIR:
- create ticket in Incidents queue (or any other queue)
  - all event fields are included in the ticket body,
  - event attributes are assigned to tickets' CFs according to the attribute mapping,
  - ticket taxonomy can be assigned according to the CF mapping. If you use taxonomy different from ENISA RSIT (https://github.com/enisaeu/Reference-Security-Incident-Taxonomy-Task-Force), consider using some extra attribute field and do value mapping with modify or sieve bot,
- create linked ticket in Investigations queue, if these conditions are met
  - if first ticket destination was Incidents queue,
  - if there is source.abuse_contact is specified,
  - if description text is specifed in the field appointed by configuration,
- RT/RTIR supposed to do relevant notifications by scrip working on condition "On Create",
- configuration option investigation_fields specifies which event fields has to be included in the investigation,
- Resolve Incident ticket, according to configuration (Investigation ticket status should depend on RT scrip configuration),

Take extra caution not to overflood your ticketing system with enormous amount of tickets. Add extra filtering for that to pass only critical events to the RT, and/or deduplicating events.

Parameters:
- rt_uri, rt_user, rt_password, verify_cert -  RT API endpoint,
- queue - ticket destination queue. If set to 'Incidents', 'Investigations' ticket will be created if create_investigation is set to true,
- CF_mapping - mapping attributes-ticket CFs, e.g. 
{"event_description.text":"Description","source.ip":"IP","extra.classification.type":"Incident Type","classification.taxonomy":"Classification"}
- final_status - what is final status for the created ticket, e.g. 'resolve' if you want to resolve created ticket. Investigation ticket will be resolved automatically by RTIR scrip,
- create_investigation - should we create Investigation ticket (in case of RTIR workflow). true or false,
- investigation_fields - attributes to include into investigation ticket, e.g. time.source,source.ip,source.port,source.fqdn,source.url,classification.taxonomy,classification.type,classification.identifier,event_description.url,event_description.text,malware.name,protocol.application,protocol.transport
- description_attr - which event attribute contains text message being sent to the recipient. If it is not specified or not found in the event, Investigation ticket is not going to be created. Example: extra.message.text,

