# sanitize

Scan staged or committed files for secrets and sensitive data before pushing.

## Usage

```
/sanitize [path]
```

## Steps

1. Search the target path (default: entire repo) for patterns that indicate secrets:
   - Passwords / credentials (`password`, `passwd`, `secret`)
   - API keys and tokens (long hex or base64 strings, `api_key`, `token`)
   - Private keys (`-----BEGIN … PRIVATE KEY-----`)
   - Real IP addresses of production equipment
   - Personal contact information (email, phone)

2. Report each finding with file path, line number, and the matched pattern.

3. For each finding, suggest the correct placeholder:
   - Passwords → `<PASSWORD-HERE>`
   - Tokens / keys → `<TOKEN-HERE>`
   - IPs → `<IP-HERE>`

4. Do **not** auto-fix — present findings and let the user decide.

## Notes

- Follows the security rules in `CLAUDE.md`.
- False positives (e.g., example placeholders) can be ignored after review.
