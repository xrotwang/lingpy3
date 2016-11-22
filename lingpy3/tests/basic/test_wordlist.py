# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase


class Tests(TestCase):
    def _make_one(self, header=None, rows=None, **kw):
        from lingpy3.basic.wordlist import Wordlist

        return Wordlist(
            ['id', 'concept', 'doculect'] if header is None else header,
            [['1', 'c1', 'l1']] if rows is None else rows,
            **kw)

    def test_init(self):
        self._make_one()

        # invalid data type for header:
        with self.assertRaises(ValueError):
            self._make_one(header=['id', 'concept', 'doculect', 5])

        # duplicate column names in header:
        with self.assertRaises(ValueError):
            self._make_one(header=['id', 'concept', 'doculect', 'id'])

        # missing columns in header:
        with self.assertRaises(ValueError):
            self._make_one(header=[])

        # row length not matching header length:
        with self.assertRaises(ValueError):
            self._make_one(rows=[[1, 2]])

        # duplicate row ID:
        with self.assertRaises(ValueError):
            self._make_one(rows=[[1, 2, 3], [1, 2, 3]])

    def test_add_col(self):
        wl = self._make_one()

        with self.assertRaises(ValueError):
            wl.add_col('id', lambda x: 'x')

        wl.add_col('xcol', lambda x: 'x')
        self.assertEqual(wl['1', 'xcol'], 'x')
        self.assertEqual(wl.header[-1], 'xcol')

        with self.assertRaises(ValueError):
            wl.add_col('xcol', lambda x: 'x')

        wl.add_col('xcol', lambda x: 'y', override=True)
        self.assertEqual(wl['1', 'xcol'], 'y')

        wl.add_col('zcol', lambda x: x['xcol'])
        self.assertEqual(wl['1', 'zcol'], 'y')
