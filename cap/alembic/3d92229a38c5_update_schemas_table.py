#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Update schemas table."""

import sqlalchemy as sa
from alembic import op

from cap.types import json_type

# revision identifiers, used by Alembic.
revision = '3d92229a38c5'
down_revision = 'f93f479d43f1'
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    op.add_column(
        'schema',
        sa.Column('created',
                  sa.DateTime(),
                  nullable=False,
                  server_default=sa.func.current_timestamp()))
    op.add_column('schema',
                  sa.Column('deposit_mapping', json_type, nullable=True))
    op.add_column('schema',
                  sa.Column('deposit_options', json_type, nullable=True))
    op.add_column('schema',
                  sa.Column('deposit_schema', json_type, nullable=True))
    op.add_column(
        'schema',
        sa.Column('is_indexed',
                  sa.Boolean(create_constraint=False),
                  nullable=True))
    op.add_column('schema',
                  sa.Column('record_mapping', json_type, nullable=True))
    op.add_column('schema',
                  sa.Column('record_options', json_type, nullable=True))
    op.add_column('schema', sa.Column('record_schema',
                                      json_type,
                                      nullable=True))
    op.add_column(
        'schema',
        sa.Column('updated',
                  sa.DateTime(),
                  nullable=False,
                  server_default=sa.func.current_timestamp()))
    op.add_column(
        'schema',
        sa.Column('use_deposit_as_record',
                  sa.Boolean(create_constraint=False),
                  nullable=True))
    op.drop_column('schema', 'json')
    op.drop_column('schema', 'is_deposit')


def downgrade():
    """Downgrade database."""
    op.add_column(
        'schema',
        sa.Column('is_deposit',
                  sa.BOOLEAN(),
                  autoincrement=False,
                  nullable=True))
    op.add_column(
        'schema',
        sa.Column('json', json_type, autoincrement=False, nullable=True))
    op.drop_column('schema', 'use_deposit_as_record')
    op.drop_column('schema', 'updated')
    op.drop_column('schema', 'record_schema')
    op.drop_column('schema', 'record_options')
    op.drop_column('schema', 'record_mapping')
    op.drop_column('schema', 'is_indexed')
    op.drop_column('schema', 'deposit_schema')
    op.drop_column('schema', 'deposit_options')
    op.drop_column('schema', 'deposit_mapping')
    op.drop_column('schema', 'created')
