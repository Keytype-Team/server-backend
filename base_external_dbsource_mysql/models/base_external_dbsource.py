# Copyright 2011 Daniel Reis
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import sqlalchemy
from sqlalchemy import text

from odoo import fields, models


class BaseExternalDbsource(models.Model):
    """It provides logic for connection to a MySQL data source."""

    _inherit = "base.external.dbsource"

    connector = fields.Selection(
        selection_add=[("mysql", "MySQL")],
        ondelete={"mysql": "cascade"},
    )

    def connection_close_mysql(self, connection):
        return connection.close()

    def connection_open_mysql(self):
        return sqlalchemy.create_engine(self.conn_string_full).connect()

    def execute_mysql(self, sqlquery, sqlparams, metadata):
        rows, cols = list(), list()
        for record in self:
            with record.connection_open() as connection:
                # SQLAlchemy 2.0+ requires text() wrapper for raw SQL strings
                stmt = text(sqlquery)
                if sqlparams is None:
                    cur = connection.execute(stmt)
                else:
                    cur = connection.execute(stmt, sqlparams)
                if metadata:
                    cols = list(cur.keys())
                rows = [r for r in cur]
        return rows, cols
