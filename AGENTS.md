# AGENTS.md

## Project

- This is a single-file Python 3 CLI: `fck.py`; dependencies are listed in `requirements.txt`.
- Install dependencies with `python3 -m pip install -r requirements.txt`.
- Run it with `python3 fck.py <URL> [delay]`; when `delay` is omitted, the script defaults to `5`.

## Verification

- There are no linters, formatters, build steps, CI workflows, or other automated checks in this repository.
- Run the live integration test with `python3 -m unittest discover -s tests`; it requires network access to `https://fckaf.de/` and checks `https://example.com` with delay `9` returns `https://fckaf.de/KZu`.
- At minimum, run `python3 -m py_compile fck.py` after Python changes.

## Implementation Constraints

- `getTokens()` first fetches the service homepage for both the CSRF token and session cookie; `getShort()` must submit them together in the subsequent request.
- `main()` catches every exception and prints only a generic error, so temporarily inspect or narrow exception handling when debugging failures.
