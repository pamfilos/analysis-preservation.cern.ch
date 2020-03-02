"""Initialize extension."""

from __future__ import absolute_import, print_function
from cap.modules.schemas.models import Schema
from invenio_search import current_search


class CAPDeposit(object):
    """CAPDeposit extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        app.extensions['cap_deposit'] = self
