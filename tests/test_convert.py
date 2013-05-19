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
            ("select '%', ?", (10,), ('%', 10)), ]:
            test(*t)

    def test_execute_named(self):
        def test(query, args, res):
            cur = self.conn.cursor()
            cur.execute(query, args)
            self.assertEqual(cur.fetchone(), res)

        for t in [
            ("select :foo, :bar", {'foo': 10, 'bar': 'asdf'}, (10, 'asdf')),
            ("select :foo::::int", {'foo': '10'}, (10,)),
            ("select '%', :foo", {'foo': 10}, ('%', 10)), ]:
            test(*t)

    def test_executemany(self):
        cur = self.conn.cursor()
        cur.execute("create table testexmany (id int, data text)")
        data = [(1, 'foo'), (2, 'bar'), (3, 'baz')]
        cur.executemany("insert into testexmany values (?, ?)",
            iter(data))
        cur.execute("select * from testexmany order by id")
        self.assertEqual(cur.fetchall(), data)


if __name__ == '__main__':
    unittest.main()
