# Contributing & Delivery Workflow

## Branching

Use short feature branches such as `feature/text-classifier`, `feature/image-explainer`, or `fix/api-validation`.

## Commit Convention

Prefer concise conventional commits:

- `feat:` new capability
- `fix:` defect correction
- `docs:` documentation
- `test:` tests
- `refactor:` internal improvement
- `chore:` tooling/configuration

## Pull Requests

Every PR should include:

1. Scope and objective
2. Key implementation changes
3. Validation performed
4. Known limitations
5. Screenshots or API examples when UI/API behavior changes

## Security

Never commit API keys, passwords, production `.env` files, personal data, private datasets, model credentials, or generated upload media.

## Quality Gate

Before delivery, run backend tests, verify the frontend build, validate API health, and update the changelog when the user-facing behavior changes.
