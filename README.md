# fckafde_cli
An unofficial CLI tool for using the https://fckaf.de/ service. It is very good. Smiley.

## Usage
Install required modules:

```bash
python3 -m pip install -r requirements.txt
```

Then type ``python3 fck.py <URL> [delay]``. If omitted, ``delay`` defaults to ``5``.

## Tests

Run the live integration test with:

```bash
python3 -m unittest discover -s tests
```

The test contacts ``https://fckaf.de/`` and requires network access. It checks
that ``https://example.com`` with a delay of ``9`` returns
``https://fckaf.de/KZu``.
