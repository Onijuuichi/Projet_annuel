import unittest


def bg():
    return "bg";



print("bgggggg")


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(bg(), "bg")  # add assertion here


if __name__ == '__main__':
    unittest.main()
