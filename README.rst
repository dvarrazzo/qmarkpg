A psycopg2 wrapper using the qmark parameters style
===================================================

The qmarkpg package is a psycopg2_ wrapper allowing the use of "qmark"
placeholders style for query arguments (i.e. ``?`` instead of ``%s``).
There is no support for parameters dictionaries: only positional parameters
are allowed.

Adopting "qmark" and dropping support for "format" (*i.e.* ``%s``) and
"pyformat" (*i.e.* ``%(name)s``) placeholders is not in program for future
Psycopg versions; however, maintainers of multi-database environments may find
the "qmark" placeholder style more useful for cross-database compatibility:
this module is designed to support such requirement without requiring
extensive rewriting of application directly using psycopg2.

.. _psycopg2: http://initd.org/psycopg/
