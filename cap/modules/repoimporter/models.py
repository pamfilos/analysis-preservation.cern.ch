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
"""Models for Git repositories and snapshots."""

from __future__ import absolute_import, print_function

from invenio_accounts.models import User
from invenio_db import db
from invenio_records.models import RecordMetadata
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils.types import UUIDType

from cap.types import json_type


class GitRepository(db.Model):
    """Information about a GitHub repository."""

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, unique=False, nullable=False)

    host = db.Column(db.String(255), nullable=False)
    owner = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    branch = db.Column(db.String(255), nullable=False, default='master')

    __tablename__ = 'git_repository'
    __table_args__ = db.UniqueConstraint(
        'host',
        'owner',
        'name',
        'branch',
        name='uq_git_repository_unique_constraint'),

    @classmethod
    def create_or_get(cls, external_id, host, owner, name, branch='master'):
        """."""
        try:
            repo = cls.query.filter_by(host=host,
                                       owner=owner,
                                       name=name,
                                       branch=branch).one()
        except NoResultFound:
            repo = cls(external_id=external_id,
                       host=host,
                       owner=owner,
                       name=name,
                       branch=branch)
            db.session.add(repo)
        return repo


class GitWebhook(db.Model):
    """Webook for a Git repository."""

    __tablename__ = 'git_webhook'
    __table_args__ = db.UniqueConstraint(
        'event_type', 'repo_id', name='uq_git_webhook_unique_constraint'),

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255), nullable=False)

    external_id = db.Column(db.String(255), nullable=False)
    secret = db.Column(db.String(32), nullable=True)

    repo_id = db.Column(db.Integer, db.ForeignKey(GitRepository.id))
    repo = db.relationship(GitRepository,
                           backref=db.backref("webhooks",
                                              cascade="all, delete-orphan"))


class GitWebhookSubscriber(db.Model):
    """Records subscribed to the git repository events."""

    __tablename__ = 'git_subscriber'
    __table_args__ = db.UniqueConstraint(
        'record_id',
        'webhook_id',
        name='uq_git_webhook_subscriber_unique_constraint'),

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('notify', 'download', name='git_event_type'),
                     nullable=False)

    status = db.Column(db.Enum('active', 'deleted', name='git_webhook_status'),
                       nullable=False,
                       default='active')

    record_id = db.Column(UUIDType,
                          db.ForeignKey(RecordMetadata.id),
                          nullable=False)
    record = db.relationship(RecordMetadata,
                             backref=db.backref("webhooks",
                                                cascade="all, delete-orphan"))

    webhook_id = db.Column(db.Integer,
                           db.ForeignKey(GitWebhook.id),
                           nullable=False)
    webhook = db.relationship(GitWebhook,
                              backref=db.backref("subscribers",
                                                 cascade="all, delete-orphan"))

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

    @property
    def repo(self):
        return self.webhook.repo


class GitSnapshot(db.Model):
    """Snapshot information for a Git repo."""

    __tablename__ = 'git_snapshot'

    id = db.Column(db.Integer, primary_key=True)

    # webhook payload / event
    payload = db.Column(json_type, default={}, nullable=True)

    # git specifics
    tag = db.Column(db.String(255), nullable=True)
    ref = db.Column(db.String(255), nullable=True)

    # foreign keys (connecting to repo and events)
    webhook_id = db.Column(db.Integer,
                           db.ForeignKey(GitWebhook.id),
                           nullable=False)
    webhook = db.relationship(GitWebhook,
                              backref=db.backref("snapshots",
                                                 cascade="all, delete-orphan"))
    created = db.Column(db.DateTime, server_default=db.func.now())

    @staticmethod
    def create(webhook, data):
        snapshot = GitSnapshot(payload=data,
                               webhook_id=webhook.id,
                               tag=data['commit'].get('tag'),
                               ref=data['commit']['id'])
        db.session.add(snapshot)
        db.session.commit()
