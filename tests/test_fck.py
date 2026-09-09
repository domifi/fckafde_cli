import contextlib
import io
import unittest
from unittest.mock import Mock, patch

from fck import getArgs, getShort


class FckafdeIntegrationTest(unittest.TestCase):
    def test_known_url_returns_known_short_url(self):
        self.assertEqual(
            getShort('https://example.com', 9),
            'https://fckaf.de/KZu',
        )


class FckafdeUnitTest(unittest.TestCase):
    def test_get_args_requires_target(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                getArgs([])

    def test_get_args_defaults_delay(self):
        args = getArgs(['https://example.com'])

        self.assertEqual(args.target, 'https://example.com')
        self.assertEqual(args.delay, 5)

    @patch('fck.requests.post')
    @patch('fck.requests.get')
    def test_get_short_uses_timeout_and_checks_responses(self, mock_get, mock_post):
        homepage = Mock()
        homepage.content = b'<input id="csrf_token" value="token">'
        homepage.cookies.get_dict.return_value = {'session': 'session-id'}
        answer = Mock()
        answer.content = b'<input id="link" value="https://fckaf.de/short">'
        mock_get.return_value = homepage
        mock_post.return_value = answer

        result = getShort('https://example.com', 9)

        self.assertEqual(result, 'https://fckaf.de/short')
        homepage.raise_for_status.assert_called_once_with()
        answer.raise_for_status.assert_called_once_with()
        mock_get.assert_called_once_with('https://fckaf.de/', timeout=10)
        mock_post.assert_called_once_with(
            'https://fckaf.de/',
            data={
                'csrf_token': 'token',
                'target': 'https://example.com',
                'delay': 9,
                'submit': 'Speichern',
            },
            headers={'Cookie': 'session=session-id'},
            timeout=10,
        )


if __name__ == '__main__':
    unittest.main()
