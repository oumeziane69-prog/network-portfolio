# changelog-generator

Generate a structured CHANGELOG entry from recent git commits.

## Usage

```
/changelog-generator [version]
```

## Steps

1. Run `git log --oneline <range>` to collect commits since the last tag or provided range.
2. Group commits by type: `feat`, `fix`, `docs`, `chore`, `refactor`.
3. Format the output as a Keep-a-Changelog section:

```markdown
## [<version>] - YYYY-MM-DD

### Added
- ...

### Fixed
- ...

### Changed
- ...
```

4. Print the section to stdout; do **not** write to `CHANGELOG.md` automatically — let the user review first.

## Notes

- Skip merge commits and bot commits.
- Use placeholders (`<version>`, `<date>`) when not supplied.
