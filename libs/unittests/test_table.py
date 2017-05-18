import unittest
import numpy as np
from libs import table

class test_table(unittest.TestCase):
    def make_table1(self):
        table1 = table.table()
        table1.insert_columns(['A', 'B', 'C'])
        table1.insert_row(A=1, B=2, C=3)
        table1.insert_row(A=3, B=2, C=1)
        table1.insert_row(A=1, B=3, C=2)
        return table1

    def test_table_1(self):
        table1 = self.make_table1()
        self.assertEqual(table1.get_column_headers(), ['A', 'B', 'C'])
        rows = [[1, 2, 3], [3, 2, 1], [1, 3, 2]]
        for entry, row in zip(table1.get_entries(), rows):
            self.assertEqual(entry.get_values(), row)

        self.assertEqual(table1.get_keyword_cwidths(), [1, 1, 1])
        self.assertEqual(table1.get_entries_cwidth('A'), 1)
        self.assertEqual(table1.get_entries_cwidth('B'), 1)
        self.assertEqual(table1.get_entries_cwidth('C'), 1)
        self.assertEqual(table1.get_entries_cwidths(), [1, 1, 1])
        self.assertEqual(table1.get_column_widths(), [1, 1, 1])
    def test_table_2(self):
        table1 = self.make_table1()
        table1.insert_column('D')
        self.assertEqual(table1.get_column_headers(), ['A', 'B', 'C', 'D'])
        rows = [[1, 2, 3, np.nan], [3, 2, 1, np.nan], [1, 3, 2, np.nan]]
        for entry, row in zip(table1.get_entries(), rows):
            self.assertEqual(entry.get_values(), row)

        self.assertEqual(table1.get_keyword_cwidths(), [1, 1, 1, 1])
        self.assertEqual(table1.get_entries_cwidth('A'), 1)
        self.assertEqual(table1.get_entries_cwidth('B'), 1)
        self.assertEqual(table1.get_entries_cwidth('C'), 1)
        self.assertEqual(table1.get_entries_cwidth('D'), 3)
        self.assertEqual(table1.get_entries_cwidths(), [1, 1, 1, 3])
        self.assertEqual(table1.get_column_widths(), [1, 1, 1, 3])

    def test_table_3(self):
        table2 = table.table()
        table2.load('test_table2.dat')
        self.assertEqual(table2.get_column_headers(), ['ID', 'Name', 'Color'])
        rows = [['2', 'Roberto', 'Blue'], ['4', 'Frank', 'Green'], ['3', 'Chad', 'Red'],\
                ['1', 'Dan', 'Green'], ['5', 'Filipe', 'Blue']]
        for entry, row in zip(table2.get_entries(), rows):
            self.assertEqual(entry.get_values(), row)


if __name__ == '__main__':
    unittest.main()
