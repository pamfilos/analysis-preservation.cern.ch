"""Access blueprint in order to dispatch the login request."""

from __future__ import absolute_import, print_function

from collections import deque

from flask import Blueprint, g, redirect, session, url_for
from flask_login import current_user
from flask_principal import AnonymousIdentity, Identity, RoleNeed
from invenio_oauthclient.signals import account_setup_received


access_blueprint = Blueprint('access', __name__,
                             url_prefix='/access',
                             template_folder='templates')


@access_blueprint.route('/login/')
def login():
    """Redirect the login request to CERN OAuth login or CAP home page."""
    if not current_user.is_authenticated:
        return redirect(url_for("invenio_oauthclient.login",
                                remote_app='cern'))
    return redirect(url_for('front.home'))


@access_blueprint.record_once
def init(state):
    """Sets the identity loader and saver for the current application."""
    principal = state.app.extensions['security'].principal
    principal.identity_loaders = deque([identity_loader_session])
    principal.identity_savers = deque([identity_saver_session])


def identity_loader_session():
    """Loads the identity session."""
    if 'identity.id' in session:
        result = Identity(session['identity.id'])
        result.auth_type = session.get('identity.auth_type')
        result.provides = set(session.get('identity.provides')) or set()
    else:
        result = AnonymousIdentity()
    return result


def identity_saver_session(identity):
    """Store the identity session."""
    session['identity.id'] = identity.id
    session['identity.auth_type'] = identity.auth_type
    session['identity.provides'] = list(identity.provides)


@account_setup_received.connect
def oauth_response(remote, token=None, response=None, account_setup=None):
    """Adds the current identity provides using the OAuth information"""
    # Requests of all the information about the current user.
    me = remote.get('https://oauthresource.web.cern.ch/api/Me')
    # Gets the relation between e-groups and concrete roles.
    egroups_roles_relations = get_egroups_roles_relations()
    # For each item in the user information response, if it is a "Group" item,
    # we add the needs allowed to that group.
    for item in me.data:
        if item['Type'] == 'http://schemas.xmlsoap.org/claims/Group':
            g.identity.provides |= set(egroups_roles_relations.get(item['Value'], []))
    identity_saver_session(g.identity)


def get_egroups_roles_relations():
    # Dictionary linking e-group with concrete roles
    result = {
        'alice_TODO': [RoleNeed('collaboration_alice')],
        'atlas_TODO': [RoleNeed('collaboration_atlas')],
        'cms-users': [RoleNeed('collaboration_cms')],
        'lhcb_TODO': [RoleNeed('collaboration_lhcb')],
    }

    # In the case of CAP developer, they have all the possible roles.
    all_roles = []
    for item in result.values():
        all_roles += item
    result['DAPF-development'] = all_roles

    return result
