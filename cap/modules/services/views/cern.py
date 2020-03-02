# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2018 CERN.
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


"""CAP CERN service views."""

import ldap
from ldap import LDAPError
from flask import jsonify, request

from . import blueprint
from cap.modules.access.utils import login_required


LDAP_SERVER_URL = 'ldap://xldap.cern.ch'

LDAP_USER_RESP_FIELDS = [
    'cn',
    'displayName',
    'mail',
    'memberOf',
    'company',
    'department',
    'cernAccountType',
    'objectClass'
]

LDAP_EGROUP_RESP_FIELDS = [
    'cn',
    'displayName',
    'description',
    'mail',
    'member',
    'objectClass'
]


def _ldap(query, sf=None, by=None):
    """LDAP user depending on the query type."""
    lc = ldap.initialize(LDAP_SERVER_URL)

    # different arguments depending on the query type
    if by == 'mail':
        ldap_fields = ['mail']  # LDAP_USER_RESP_FIELDS alternative
        search_at = 'OU=Users,OU=Organic Units,DC=cern,DC=ch'
        ldap_query = '(&(cernAccountType=Primary)(mail=*{}*))' \
            .format(query)
    else:
        ldap_fields = LDAP_EGROUP_RESP_FIELDS
        search_at = 'OU=e-groups,OU=Workgroups,DC=cern,DC=ch'
        ldap_query = '{}=*{}*'.format(sf, query)

    try:
        lc.search_ext(
            search_at, ldap.SCOPE_ONELEVEL, ldap_query, ldap_fields,
            serverctrls=[ldap.controls.SimplePagedResultsControl(
                True, size=7, cookie='')
            ]
        )
        status = 200
        data = lc.result()[1]
    except LDAPError as err:
        status = 500
        data = err.message

    return data, status


@blueprint.route('/ldap/user/mail')
@login_required
def ldap_user_by_mail():
    """LDAP user by username query."""
    query = request.args.get('query', None)

    if not query:
        return jsonify([])

    resp, status = _ldap(query, by='mail')
    data = [x[1]['mail'][0] for x in resp]
    return jsonify(data)


@blueprint.route('/ldap/egroup/mail')
@login_required
def ldap_egroup_mail():
    """LDAP egroup query."""
    query = request.args.get('query', None)
    sf = request.args.get('sf', 'cn')

    if not query:
        return jsonify([])

    resp, status = _ldap(query, sf, by='egroup')
    data = [x[1]['mail'][0] for x in resp]
    return jsonify(data)
