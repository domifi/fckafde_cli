import contextlib
import io
import unittest
from unittest.mock import Mock, call, patch

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
        self.assertEqual(args.delay, 3)

    @patch('fck.requests.Session')
    def test_get_short_uses_session_timeout_and_checks_responses(self, mock_session):
        session = Mock()
        mock_session.return_value.__enter__.return_value = session
        homepage = Mock()
        homepage.content = (
            b'<input id="csrf_token" value="token">'
            b'<select id="delay">'
            b'<option value="00">00</option>'
            b'<option value="03">03</option>'
            b'<option value="06">06</option>'
            b'<option value="09">09</option>'
            b'</select>'
        )
        answer = Mock()
        answer.content = b'<input id="link" value="https://fckaf.de/short">'
        session.get.return_value = homepage
        session.post.return_value = answer

        result = getShort('https://example.com', 9)

        self.assertEqual(result, 'https://fckaf.de/short')
        mock_session.assert_called_once_with()
        homepage.raise_for_status.assert_called_once_with()
        answer.raise_for_status.assert_called_once_with()
        session.get.assert_called_once_with('https://fckaf.de/', timeout=10)
        session.post.assert_called_once_with(
            'https://fckaf.de/',
            data={
                'csrf_token': 'token',
                'target': 'https://example.com',
                'delay': '09',
                'submit': 'Speichern',
            },
            timeout=10,
        )
        request_calls = [
            mock_call for mock_call in session.mock_calls
            if mock_call[0] in ('get', 'post')
        ]
        self.assertEqual(request_calls, [
            call.get('https://fckaf.de/', timeout=10),
            call.post(
                'https://fckaf.de/',
                data={
                    'csrf_token': 'token',
                    'target': 'https://example.com',
                    'delay': '09',
                    'submit': 'Speichern',
                },
                timeout=10,
            ),
        ])

    @patch('fck.requests.Session')
    def test_get_short_rounds_unavailable_delay(self, mock_session):
        session = Mock()
        mock_session.return_value.__enter__.return_value = session
        homepage = Mock()
        homepage.content = (
            b'<input id="csrf_token" value="token">'
            b'<select id="delay">'
            b'<option value="00">00</option>'
            b'<option value="03">03</option>'
            b'<option value="06">06</option>'
            b'<option value="09">09</option>'
            b'</select>'
        )
        answer = Mock()
        answer.content = b'<input id="link" value="https://fckaf.de/short">'
        session.get.return_value = homepage
        session.post.return_value = answer
        stderr = io.StringIO()

        with contextlib.redirect_stderr(stderr):
            getShort('https://example.com', 5)

        session.post.assert_called_once_with(
            'https://fckaf.de/',
            data={
                'csrf_token': 'token',
                'target': 'https://example.com',
                'delay': '06',
                'submit': 'Speichern',
            },
            timeout=10,
        )
        self.assertIn(
            'Requested delay of 5 seconds is unavailable; using 6 seconds instead.',
            stderr.getvalue(),
        )


if __name__ == '__main__':
    unittest.main()
