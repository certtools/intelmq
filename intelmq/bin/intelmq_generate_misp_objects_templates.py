#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a MISP object template
see https://github.com/MISP/misp-objects/
"""
import json
from pathlib import Path
from uuid import uuid4
import argparse


class MISPObjectTemplateGenerator:

    def __init__(self, object_templates_path: Path, harmonization_file_path: Path):
        intelmq_event_template_name = 'intelmq_event'
        intelmq_report_template_name = 'intelmq_report'
        event_template_dir = object_templates_path / 'objects' / intelmq_event_template_name
        report_template_dir = object_templates_path / 'objects' / intelmq_report_template_name
        event_template_dir.mkdir(exist_ok=True)
        report_template_dir.mkdir(exist_ok=True)

        self.event_template_path = event_template_dir / 'definition.json'
        if self.event_template_path.exists():
            with self.event_template_path.open() as f:
                self.misp_object_intelmq_event = json.load(f)
            self.misp_object_intelmq_event['version'] += 1
        else:
            self.misp_object_intelmq_event = {
                'name': intelmq_event_template_name,
                'uuid': str(uuid4()),
                'meta-category': 'network',
                'description': 'IntelMQ Event',
                'version': 1,
                'attributes': {}
            }

        self.report_template_path = report_template_dir / 'definition.json'
        if self.report_template_path.exists():
            with self.report_template_path.open() as f:
                self.misp_object_intelmq_report = json.load(f)
            self.misp_object_intelmq_report['version'] += 1
        else:
            self.misp_object_intelmq_report = {
                'name': intelmq_report_template_name,
                'uuid': str(uuid4()),
                'meta-category': 'network',
                'description': 'IntelMQ Report',
                'version': 1,
                'attributes': {}
            }

        with harmonization_file_path.open() as f:
            self.intelmq_fields = json.load(f)

    def _intelmq_misp_mapping(self, content, object_relation):
        attribute = {'description': content['description'], 'ui-priority': 1}
        if content['type'] in ['String', 'LowercaseString', 'ClassificationType',
                               'UppercaseString', 'Registry', 'JSONDict', 'JSON',
                               'TLP', 'Base64']:
            attribute['misp-attribute'] = 'text'
        elif content['type'] == 'DateTime':
            attribute['misp-attribute'] = 'datetime'
        elif content['type'] == 'ASN':
            attribute['misp-attribute'] = 'AS'
        elif content['type'] == 'FQDN':
            attribute['misp-attribute'] = 'text'
        elif content['type'] == 'Float':
            attribute['misp-attribute'] = 'float'
        elif (content['type'] in ['IPAddress', 'IPNetwork'] and
              object_relation.startswith('destination')):
            attribute['misp-attribute'] = 'ip-dst'
        elif (content['type'] in ['IPAddress', 'IPNetwork'] and
              object_relation.startswith('source')):
            attribute['misp-attribute'] = 'ip-src'
        elif content['type'] == 'Integer':
            attribute['misp-attribute'] = 'counter'
        elif content['type'] == 'Boolean':
            attribute['misp-attribute'] = 'boolean'
        elif content['type'] == 'URL':
            attribute['misp-attribute'] = 'url'
        elif content['type'] == 'Accuracy':
            attribute['misp-attribute'] = 'float'
        else:
            raise Exception('Unknown type {content["type"]}: {object_relation} - {content}')
        return attribute

    def generate_templates(self):
        for object_relation, content in self.intelmq_fields['event'].items():
            self.misp_object_intelmq_event['attributes'].update(
                {object_relation: self._intelmq_misp_mapping(content, object_relation)}
            )

        for object_relation, content in self.intelmq_fields['report'].items():
            self.misp_object_intelmq_report['attributes'].update(
                {object_relation: self._intelmq_misp_mapping(content, object_relation)}
            )

    def dump_templates(self):
        with self.event_template_path.open('w') as f:
            json.dump(self.misp_object_intelmq_event, f, indent=2, sort_keys=True)
        with self.report_template_path.open('w') as f:
            json.dump(self.misp_object_intelmq_report, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate or update MISP object templates.')
    parser.add_argument("--objects", required=True,
                        help="Path to misp-objects repository. "
                             "The generated template will be written to this path or updated in this path.")
    parser.add_argument("--harmonization", required=True,
                        help="Path to harmonization.conf to be used.")
    args = parser.parse_args()

    objects = Path(args.objects)
    if not objects.exists():
        raise Exception('Path to misp-objects repository does not exists: {args.objects}'.format(args=args))

    harmonization_file = Path(args.harmonization)
    if not harmonization_file.exists():
        raise Exception('Path to harmonization configuration does not exists: {args.harmonization}'.format(args=args))

    g = MISPObjectTemplateGenerator(objects, harmonization_file)
    g.generate_templates()
    g.dump_templates()
