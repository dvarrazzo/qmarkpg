"""
A psycopg2 wrapper using qmark/named parameters styles
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

__version__ = '0.1'

import re
from collections import Mapping, Sequence

# Import everything from psycopg2, then override something
from psycopg2 import *
from psycopg2.extensions import connection as _connection, cursor as _cursor
paramstyle = 'named' # or qmark? whatever.
_connect = connect

RE_NAMED = re.compile(r'::|%|:[a-zA-Z0-9_]+')
RE_QMARK = re.compile(r'\?\?|\?|%')

def convert_params(query, args):
    """
    Convert a qmark query into "format" or a named query into "pyformat".

    I'm not sure it is possible to disambiguate the two query styles, I'm not
    even sure anybody has tried showing it is possible or the contrary. So we
    try to infer from the args which type of arguments the query has.
    """
    if args is None:
        # no placeholder here
        return query

    elif isinstance(args, Mapping):
        def sub_mapping(m):
            s = m.group(0)
            if s == '::':
                return ':'
            if s == '%':
                return '%%'
            else:
                return '%%(%s)s' % s[1:]

        return RE_NAMED.sub(sub_mapping, query)

    elif isinstance(args, Sequence):
        def sub_sequence(m):
            s = m.group(0)
            if s == '??':
                return '?'
            if s == '%':
                return '%%'
            else:
                return '%s'

        return RE_QMARK.sub(sub_sequence, query)

    else:
        raise TypeError('expected a sequence or mapping argument')


class QmarkNamedConnection(_connection):
    """
    A connection returning `QmarkNamedCursor` by default.
    """
    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', QmarkNamedCursor)
        return super(QmarkNamedConnection, self).cursor(*args, **kwargs)


class QmarkNamedCursor(_cursor):
    """
    A cursor using "qmark" or "named" placeholders for queries.
    """
    def execute(self, query, args=None):
        query = convert_params(query, args)
        return super(QmarkNamedCursor, self).execute(query, args)

    def executemany(self, query, args_seq):
        # pull out the first args to help sniffing the placeholder
        args_seq = iter(args_seq)
        try:
            args = args_seq.next()
        except StopIteration:
            return

        # helper to re-join the first args and the others in a single iterator
        def join(args, args_seq):
            yield args
            for args in args_seq:
                yield args

        query = convert_params(query, args)
        return super(QmarkNamedCursor, self).executemany(
            query, join(args, args_seq))

    def callproc(self, query, args=None):
        query = convert_params(query, args)
        return super(QmarkNamedCursor, self).callproc(query, args)


def connect(*args, **kwargs):
    """
    Return a new database connection.

    The connection class is QmarkNamedConnection unless the connection_factory
    parameter is overridden.
    """
    kwargs.setdefault('connection_factory', QmarkNamedConnection)
    return _connect(*args, **kwargs)
