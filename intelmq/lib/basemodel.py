# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""pydantic Models for Report and Event"""

from pydantic import Field, field_validator, create_model, ConfigDict

import intelmq.lib.harmonization as harmonization
from intelmq.lib.utils import load_configuration
from intelmq.lib.message import Event, Report

__all__ = ['IntelMQReportModel', 'IntelMQEventModel']


report_harmonization = Report().harmonization_config
event_harmonization = Event().harmonization_config


def validation_wrapper(func):
    def validate(value):
        original = func(value, sanitize=True)
        if original is not True:
            raise ValueError(f'Validation failed (returned {original!r})')
    return validate


def generate_model_schema(base: dict) -> dict:
    schema = {'__validators__': {}, '__config__': ConfigDict(extra='forbid')}
    for key, value in base.items():
        harm_type = getattr(harmonization, value['type'])
        schema['__validators__'][f'{key}_validator'] = field_validator(key)(validation_wrapper(harm_type.is_valid))
        kwargs = {'default': None}
        if value['type'] in ('String', 'Base64', 'URL', 'FQDN', 'MalwareName', 'ClassificationType', 'LowercaseString', 'UppercaseString',
                             'Registry', 'TLP', 'ClassificationTaxonomy', 'UUID', 'DateTime', 'IPAddress', 'IPNetwork'):
            fieldtype = str
        elif value['type'] == 'Boolean':
            fieldtype = bool
        elif value['type'] in ('Integer', 'ASN'):
            fieldtype = int
        elif value['type'] in ('Float', 'Accuracy'):
            fieldtype = float
        elif value['type'] in ('JSON', 'JSONDict'):
            fieldtype = dict
        else:
            raise ValueError('Unknown type %r.' % value['type'])

        kwargs['description'] = f"{value['description']}\n\nType description:\n{harm_type.__doc__}"
        # Prevent pydantic throwing "TypeError: object of type 'int' has no len()" -> "Unable to apply constraint 'max_length' to supplied value [int]"
        kwargs['max_length'] = value.get('length', None) if fieldtype is str else None
        kwargs['pattern'] = value.get('regex', value.get('iregex', None))
        schema[key] = (fieldtype, Field(**kwargs))
    return schema


# https://docs.pydantic.dev/latest/api/base_model/#pydantic.create_model
IntelMQReportModel = create_model(
    "IntelMQReport",
    **generate_model_schema(report_harmonization)
)
IntelMQEventModel = create_model(
    "IntelMQEvent",
    **generate_model_schema(event_harmonization)
)
