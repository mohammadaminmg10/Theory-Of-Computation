import unittest
from degree import Degree


class TestDegreeMethod(unittest.TestCase):
    def test_get_degree(self):
        degree_1 = Degree('a***').get_degree()
        self.assertEqual(degree_1, 3)

        degree_2 = Degree('(ab)*+c*').get_degree()
        self.assertEqual(degree_2, 1)

        degree_3 = Degree('a+b').get_degree()
        self.assertEqual(degree_3, 0)

        degree_4 = Degree('').get_degree()
        self.assertEqual(degree_4, 0)

        degree_5 = Degree('a').get_degree()
        self.assertEqual(degree_5, 0)

        degree_6 = Degree('λ').get_degree()
        self.assertEqual(degree_6, 0)


if __name__ == '__main__':
    unittest.main()
