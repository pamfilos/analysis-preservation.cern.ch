# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2017 CERN.
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
# or submit itself to any jurisdiction.
"""Unit tests for Cap Deposit class."""

from uuid import uuid4

from flask_security import login_user
from invenio_access.models import ActionUsers
from pytest import raises

from cap.modules.deposit.api import CAPDeposit as Deposit
from cap.modules.deposit.errors import DepositValidationError


def test_create_deposit_with_empty_data_raises_DepositValidationError(
        app, users, location):
    metadata = {}

    with app.test_request_context():
        login_user(users['superuser'])
        id_ = uuid4()

        with raises(DepositValidationError):
            Deposit.create(metadata, id_=id_)


def test_create_deposit_with_empty_schema_raises_DepositValidationError(
        app, users, location):
    metadata = {'$schema': ''}

    with app.test_request_context():
        login_user(users['superuser'])
        id_ = uuid4()

        with raises(DepositValidationError):
            Deposit.create(metadata, id_=id_)


def test_create_deposit_with_wrong_schema_raises_DepositValidationError(
        app, users, location):
    metadata = {
        '$schema': 'https://analysispreservation.cern.ch/schemas/deposits/records/non-existing-schema.json'  # noqa
    }

    with app.test_request_context():
        login_user(users['superuser'])
        id_ = uuid4()

        with raises(DepositValidationError):
            Deposit.create(metadata, id_=id_)


def test_add_user_permissions_set_access_object_properly(
        app, db, users, create_deposit):
    owner, other_user = users['cms_user'], users['cms_user2']
    deposit = create_deposit(owner, 'alice-analysis-v0.0.1')

    assert deposit['_access'] == {
        'deposit-read': {
            'users': [owner.id],
            'roles': []
        },
        'deposit-update': {
            'users': [owner.id],
            'roles': []
        },
        'deposit-admin': {
            'users': [owner.id],
            'roles': []
        }
    }

    deposit._add_user_permissions(other_user,
                                  ['deposit-read', 'deposit-update'],
                                  db.session)

    deposit = Deposit.get_record(deposit.id)

    assert deposit['_access'] == {
        'deposit-read': {
            'users': [owner.id, other_user.id],
            'roles': []
        },
        'deposit-update': {
            'users': [owner.id, other_user.id],
            'roles': []
        },
        'deposit-admin': {
            'users': [owner.id],
            'roles': []
        }
    }


def test_add_user_permissions_adds_action_to_db(app, db, users, deposit):
    user = users['cms_user']
    assert not ActionUsers.query.filter_by(action='deposit-read',
                                           argument=str(deposit.id),
                                           user_id=user.id).all()

    deposit._add_user_permissions(user, ['deposit-read'], db.session)

    assert ActionUsers.query.filter_by(action='deposit-read',
                                       argument=str(deposit.id),
                                       user_id=user.id).one()
