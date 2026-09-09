# AGENTS.md

## Project

- This is a single-file Python 3.10+ CLI: `fck.py`; dependencies are listed in `requirements.txt`.
- Install dependencies with `python3 -m pip install -r requirements.txt`.
- Run it with `python3 fck.py <URL> [delay]`; when `delay` is omitted, the script defaults to `3`.

## Verification

- There are no linters, formatters, or build steps in this repository. CI runs the test workflow on pushes and pull requests.
- Run the live integration test with `python3 -m unittest discover -s tests`; it requires network access to `https://fckaf.de/` and checks `https://example.com` with delay `9` returns `https://fckaf.de/KZu`.
- The CI workflow is `.github/workflows/test.yaml`; Forgejo uses this file when `.forgejo/workflows` is absent. Its runner must provide the `ubuntu-latest` label and outbound network access.
- At minimum, run `python3 -m py_compile fck.py` after Python changes.

## Implementation Constraints

- `getShort()` must use one `requests.Session` for the homepage GET that obtains the CSRF token and session cookie and the subsequent shortening POST.
- The homepage `<select id="delay">` defines the allowed delays; `getShort()` rounds the requested delay to the nearest allowed value, prints a stderr note when it changes it, and posts the exact option string (e.g. `09`).
- `main()` reports runtime failures only as a generic stderr message; temporarily inspect or narrow exception handling when debugging failures.
