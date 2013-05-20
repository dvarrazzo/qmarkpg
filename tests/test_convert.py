from testutils import unittest, ConnectingTestCase

class ConvertTestCase(ConnectingTestCase):
    def test_execute_qmark(self):
        def test(query, args, res):
            cur = self.conn.cursor()
            cur.execute(query, args)
            self.assertEqual(cur.fetchone(), res)

        for t in [
            ("select ?, ?", (10, 'asdf'), (10, 'asdf')),
            ("select '??', ?", (10,), ('?', 10)),
            ("select '%', ?", (10,), ('%', 10)),
            ("select '%'", (), ('%',)),
            ("select '%'", None, ('%',)), ]:
            test(*t)

    def test_executemany(self):
        cur = self.conn.cursor()
        cur.execute("create table testexmany (id int, data text)")
        data = [(1, 'foo'), (2, 'bar'), (3, 'baz')]
        cur.executemany("insert into testexmany values (?, ?)",
            iter(data))
        cur.execute("select * from testexmany order by id")
        self.assertEqual(cur.fetchall(), data)

    def test_no_format(self):
        cur = self.conn.cursor()
        self.assertRaises(self.conn.ProgrammingError,
            cur.execute, "select %s", (10,))

    def test_no_pyformat(self):
        cur = self.conn.cursor()
        self.assertRaises(self.conn.ProgrammingError,
            cur.execute, "select %(name)s", {'name': 10})

    def test_no_mapping(self):
        cur = self.conn.cursor()
        self.assertRaises(TypeError,
            cur.execute, "select ?", {'name': 10})


if __name__ == '__main__':
    unittest.main()
