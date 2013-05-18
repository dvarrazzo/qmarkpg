qmarkpg -- psycopg with qmark flavour
=====================================

This package is a psycopg2_ wrapper, allowing the use of "qmark" placeholders
style for positional arguments (i.e. ``?`` instead of ``%s``) and "named"
placeholders for mapped arguments (i.e. ``:name`` instead of ``%(name)s``.

This package is a proof of concept: adopting qmark/named placeholders is not
in program for future psycopg versions. Some multi-database environment may
find such placeholder styles more useful for cross-database compatibility.

.. _psycopg2: http://initd.org/psycopg/
