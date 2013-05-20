"""
A psycopg2 wrapper using the qmark parameters style
"""

# Copyright (C) 2013 Daniele Varrazzo  <daniele.varrazzo@gmail.com>
#
# qmarkpg is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qmarkpg is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.

__version__ = '0.2'

import re

# Import everything from psycopg2, then override something
from psycopg2 import *
from psycopg2.extensions import connection as _connection, cursor as _cursor
paramstyle = 'qmark'
_connect = connect

RE_QMARK = re.compile(r'\?\?|\?|%')

def convert_params(query):
    """
    Convert a "qmark" query into "format" style.
    """
    def sub_sequence(m):
        s = m.group(0)
        if s == '??':
            return '?'
        if s == '%':
            return '%%'
        else:
            return '%s'

    return RE_QMARK.sub(sub_sequence, query)


class QmarkConnection(_connection):
    """
    A connection returning `QmarkCursor` by default.
    """
    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', QmarkCursor)
        return super(QmarkConnection, self).cursor(*args, **kwargs)


class QmarkCursor(_cursor):
    """
    A cursor using "qmark" placeholders for queries.
    """
    def execute(self, query, args=None):
        query = convert_params(query)
        if args is None:
            # to make sure the conversion %% -> % is performed
            args = ()
        return super(QmarkCursor, self).execute(query, args)

    def executemany(self, query, args_seq):
        def denullify(args_seq):
            for args in args_seq:
                if args is not None:
                    yield args
                else:
                    yield ()

        query = convert_params(query)
        return super(QmarkCursor, self).executemany(
            query, denullify(args_seq))

    def callproc(self, query, args=None):
        query = convert_params(query)
        if args is None:
            args = ()
        return super(QmarkCursor, self).callproc(query, args)


def connect(*args, **kwargs):
    """
    Return a new database connection.

    The connection class is QmarkConnection unless the connection_factory
    parameter is overridden.
    """
    kwargs.setdefault('connection_factory', QmarkConnection)
    return _connect(*args, **kwargs)
