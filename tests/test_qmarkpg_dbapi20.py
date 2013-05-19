#!/usr/bin/env python

# test_qmarkpg_dbapi20.py - DB API conformance test for qmarkpg
#
# Copyright (C) 2006-2011 Federico Di Gregorio  <fog@debian.org>
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

import dbapi20
import dbapi20_tpc
from testutils import skip_if_tpc_disabled
from testutils import unittest, decorate_all_tests
import qmarkpg

from testconfig import dsn

class QmarkpgTests(dbapi20.DatabaseAPI20Test, unittest.TestCase):
    driver = qmarkpg
    connect_args = ()
    connect_kw_args = {'dsn': dsn}

    lower_func = 'lower' # For stored procedure test

    def test_setoutputsize(self):
        # psycopg2's setoutputsize() is a no-op
        pass

    def test_nextset(self):
        # psycopg2 does not implement nextset()
        pass


class QmarkpgTPCTests(dbapi20_tpc.TwoPhaseCommitTests, unittest.TestCase):
    driver = qmarkpg

    def connect(self):
        return qmarkpg.connect(dsn=dsn)

decorate_all_tests(QmarkpgTPCTests, skip_if_tpc_disabled)


def test_suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main()
