---
name: git-convention
description: Write conventional git commit messages following the Angular commit convention format. Use this skill whenever writing commit messages, creating commits, reviewing git history, generating changelogs, or any task involving git version control. Triggers when you see "commit", "git commit", "commit message", "changelog", "version control", "git history", "semantic commit", "conventional commit", or when the user asks to commit changes, create a PR, or review commit history. Also use when setting up commit linting or husky hooks for enforcing commit conventions.
---

# Git Convention Skill

Write conventional commit messages that are machine-readable, enable automatic changelog generation, and drive semantic versioning (`fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` → MAJOR).

## Format

```
<type>[optional scope][!]: <subject>

[optional body]

[optional footer(s)]
```

Append `!` after type/scope to flag a breaking change without a footer: `feat!:` or `feat(api)!:`.

## Type

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, whitespace (no logic change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system or dependency changes |
| `ci` | CI configuration changes |
| `chore` | Other changes not modifying src or test files |
| `revert` | Reverts a previous commit |

## Scope

The scope identifies the area of change — module, package, component, or feature name. Use lowercase, keep it short.

Examples: `auth`, `api`, `ui`, `user`, `core`, `payment`, `config`

## Subject Rules

- Imperative, present tense: "add" not "added" or "adds"
- Lowercase first letter, no period at the end
- Under 72 characters

## Body

Explain **what** changed and **why**, not how. Separate from subject with a blank line. Use bullet points for multiple changes.

## Footer

One or more footers in git trailer format (`Token: value` or `Token #value`). Common tokens:

- `Closes #123` — link to issues
- `BREAKING CHANGE: description` — note breaking API changes
- `Refs: #456` — reference related commits/PRs
- `Reviewed-by: Name` — credit reviewers

## Examples

**Feature:**
```
feat(auth): add login with Google

- Add GoogleSignInButton component
- Update auth service to handle OAuth tokens
- Handle failed authentication with error boundary

Closes #123
```

**Bug fix:**
```
fix(api): handle null response from user endpoint

Null responses crashed the app. Return empty user object instead.
```

**Breaking change (footer):**
```
feat(core): change user model structure

BREAKING CHANGE: User.id is now String instead of int.
All database queries need updating.
```

**Breaking change (`!` notation):**
```
feat(api)!: send email when product ships
```

**Refactoring:**
```
refactor(user): extract validation to separate class

Move validation from UserService to UserValidator for testability.
```

## Best Practices

**DO**:
- Use imperative mood throughout ("add", "move", "fix")
- Keep subject under 72 characters
- Explain what and why in the body
- Reference issues in the footer
- One logical change per commit

**DON'T**:
- Use past tense
- Capitalize subject or end with period
- Mix multiple types in one commit
- Write vague subjects like "update stuff"
- Explain how the code works in the message
- Add Co-Authored-By or AI attribution lines

## Tooling

These tools make conventional commits practical by automating enforcement and changelog generation. Search for the right tool based on your project's language:

**Commit linting** — reject commits that don't follow the format. Works as a git hook (often via husky, pre-commit, or lefthook).

**Changelog generation** — read commit history and produce a categorized CHANGELOG.md automatically:
- `feat` → Features section
- `fix` → Bug Fixes section
- `BREAKING CHANGE` → Breaking Changes section

Popular options by ecosystem:
- **JS/TS**: commitlint + conventional-changelog
- **Python**: commitizen
- **Flutter/Dart**: changelog_cli + conventional_commit
- **Android**: jreleaser + conventional-commit-gradle-plugin
- **Go**: goreleaser + git-chglog
- **Rust**: cog (cocogitto)
- **Ruby**: commitizen-rb
- **Java/Kotlin**: jreleaser + conventional-commit-gradle-plugin
- **.NET/C#**: GitVersion + MinVer
- **PHP**: conventional-commits-php