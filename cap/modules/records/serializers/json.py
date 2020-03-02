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
"""CAP Basic Serializers."""

from __future__ import absolute_import, print_function

from invenio_accounts.models import User
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_rest.serializers.json import JSONSerializer


class RecordSerializer(JSONSerializer):
    """Serializer for records v1 in JSON."""
    def preprocess_search_hit(self, pid, record_hit, links_factory=None):
        """Fetch PID object for records retrievals from ES."""
        pid = PersistentIdentifier.get(pid_type=pid.pid_type,
                                       pid_value=pid.pid_value)

        result = super(RecordSerializer,
                       self).preprocess_search_hit(pid,
                                                   record_hit,
                                                   links_factory=links_factory)

        return result


class BasicJSONSerializer(JSONSerializer):
    """Serializer for deposit client in JSON."""
    pass


class PermissionsJSONSerializer(JSONSerializer):
    """Serializer for returning deposit permissions in JSON."""
    def preprocess_record(self, pid, record, links_factory=None, **kwargs):
        """Remove unnecessary values for client."""
        result = super(PermissionsJSONSerializer,
                       self).preprocess_record(pid,
                                               record,
                                               links_factory=links_factory)

        result['permissions'] = result.get('metadata', {}).get('_access', {})

        for k, v in result['permissions'].items():
            if v['users']:
                for index, user_id in enumerate(v['users']):
                    user = User.query.filter_by(id=user_id).one()
                    v['users'][index] = user.email

        return result
