# fckafde_cli
An unofficial CLI tool for using the https://fckaf.de/ service. It is very good. Smiley.

Requires Python 3.10 or newer.

## Usage
Install required modules:

```bash
python3 -m pip install -r requirements.txt
```

Then type ``python3 fck.py <URL> [delay]``. If omitted, ``delay`` defaults to ``5``.

## Nix

Run without installing anything, using a local checkout:

```bash
nix run . -- https://example.com [delay]
```

Or directly from the repository on GitHub:

```bash
nix run github:domifi/fckafde_cli -- https://example.com [delay]
```

As with the pip install above, ``delay`` defaults to ``5`` when omitted. This
uses the pinned Python environment from ``flake.lock``, so no system Python or
pip packages are needed.

## Tests

Run the live integration test with:

```bash
python3 -m unittest discover -s tests
```

The test contacts ``https://fckaf.de/`` and requires network access. It checks
that ``https://example.com`` with a delay of ``9`` returns
``https://fckaf.de/KZu``.
