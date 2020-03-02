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
#

"""Authentication for CAP."""

from __future__ import absolute_import, print_function

from flask_login import current_user

from authlib.flask.client import OAuth
from .config import OAUTH_SERVICES
from .models import OAuth2Token
from .utils import _create_or_update_token
from invenio_db import db


def _fetch_token(name, user_id=None):
    if not user_id:
        user_id = current_user.id
    token = OAuth2Token.get(name=name, user_id=user_id)
    return token.to_token() if token else None


def _update_token(name, token):
    _token = _create_or_update_token(name, token)

    db.session.add(_token)
    db.session.commit()
    return _token


class CAPOAuth(object):
    """CAP auth extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.auth = OAuth(app,
                          fetch_token=_fetch_token,
                          update_token=_update_token)
        self.register_oauth_services()
        self.app = app
        app.extensions['cap-auth'] = self

    def register_oauth_services(self):
        for service in OAUTH_SERVICES:
            self.auth.register(**OAUTH_SERVICES[service])
