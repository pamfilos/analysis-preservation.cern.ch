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
"""Models for schemas."""
from jsonschema.validators import Draft4Validator
from marshmallow import ValidationError, validate

draft4SchemaValidator = Draft4Validator(Draft4Validator.META_SCHEMA)


class JSONSchemaValidator(validate.Validator):
    """Validate JSONSchema json against corresponding draft version."""

    def __call__(self, value):
        """Wrap errors in marshmallow ValidationError."""
        # make errors compliant with marshamllow ValidationError format
        errors = {
            '.'.join(error.path): [str(error.message)]
            for error in draft4SchemaValidator.iter_errors(value)
        }
        if errors:
            raise ValidationError(message=errors)
