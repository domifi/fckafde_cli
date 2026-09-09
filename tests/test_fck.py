import unittest

from fck import getShort


class FckafdeIntegrationTest(unittest.TestCase):
    def test_known_url_returns_known_short_url(self):
        self.assertEqual(
            getShort('https://example.com', 9),
            'https://fckaf.de/KZu',
        )


if __name__ == '__main__':
    unittest.main()
