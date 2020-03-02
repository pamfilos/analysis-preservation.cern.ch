# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2016 CERN.
#
# CERN Analysis Preservation Framework is free software; you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Analysis Preservation Framework; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""CAP Basic Schemas."""

from __future__ import absolute_import, print_function

import copy

from invenio_jsonschemas import current_jsonschemas
from marshmallow import Schema, fields

from cap.modules.deposit.api import CAPDeposit
from cap.modules.records.permissions import UpdateRecordPermission

from . import common


class RecordSchema(common.CommonRecordSchema):
    """Schema for records v1 in JSON."""
    type = fields.Str(default='record')

    draft_id = fields.String(attribute='metadata._deposit.id', dump_only=True)


class RecordFormSchema(RecordSchema):
    """Schema for records v1 in JSON."""

    schemas = fields.Method('get_record_schemas', dump_only=True)
    can_update = fields.Method('can_user_update', dump_only=True)

    def get_record_schemas(self, obj):
        deposit = CAPDeposit.get_record(obj['pid'].object_uuid)

        schema = current_jsonschemas.get_schema(deposit.schema.record_path,
                                                with_refs=True,
                                                resolved=True)
        uiSchema = deposit.schema.record_options

        return dict(schema=copy.deepcopy(schema), uiSchema=uiSchema)

    def can_user_update(self, obj):
        deposit = CAPDeposit.get_record(obj['pid'].object_uuid)
        return UpdateRecordPermission(deposit).can()


class BasicDepositSchema(Schema):
    """Schema for deposit in JSON."""

    pid = fields.Str(attribute='pid.pid_value', dump_only=True)
    metadata = fields.Method('get_metadata', dump_only=True)
    created = fields.Str(dump_only=True)
    updated = fields.Str(dump_only=True)

    def get_metadata(self, obj):
        result = {
            k: v
            for k,
            v in obj.get('metadata', {}).items()
            if k not in [
                'control_number',
                '$schema',
                '_deposit',
                '_experiment',
                '_access',
                '_files',
                '_user_edited',
                '_fetched_from'
            ]
        }
        return result


class PermissionsDepositSchema(Schema):
    """Schema for files in deposit."""

    permissions = fields.Raw()


class FileSchemaV1(Schema):
    """Schema for files in deposit."""

    pass
