# CI/CD Pipeline

Numbered reusable workflows, one responsibility each, numbered by dependency
order. The number sorts them in the file tree and documents the cascade.

```text
00-install-deps  ← primes the uv cache (keyed on uv.lock)
01-ci            ← lint/format/type-check/security → test; the quality gate
02-tag-sync      ← orchestrator: CI gate → create/preview tag
```

There is **no publish stage**: flash-excel is a Windows desktop app, not a
published package. Distribution (PyInstaller build, TUF signing, upload to R2)
runs **locally** via `build.py` at the repo root — never in CI, because the
TUF signing keys are never uploaded as CI secrets. See
`[tool.ezcompiler]` in `pyproject.toml`.

## Tagging: `main` vs preview

`02-tag-sync` does **not** bump the version — a human writes it in
`pyproject.toml`. It gates every tag action on the ref:

| Ref                                | Tag                            |
| ---------------------------------- | ------------------------------ |
| push to `main`                     | create `vX.Y.Z` + `vX-latest`* |
| `workflow_dispatch` off non-`main` | **none** (preview, dry-run)    |

\* Re-running on an unchanged version is a no-op (the tag already points to
`HEAD`); it is not a separate `skip` state — it just doesn't move anything.

## Tag immutability

- **`vX.Y.Z`** — created once, **never force-pushed**. If a tag with this name
  exists and points elsewhere, the job **fails on purpose** rather than moving
  it — bump the version to release again.
- **`vX-latest`** — floating major alias, force-pushed on every release on
  `main`.

## Why a single orchestrator (`02`)

A tag pushed by `GITHUB_TOKEN` does **not** trigger another workflow (loop
protection). So `02-tag-sync` calls `01-ci` directly via `uses:` rather than
relying on a `push: tags` event that would never fire.

## CI gates the release

`auto-tag` runs `needs: ci`, where `ci: uses: ./01-ci.yml`. A failing
lint/type/security/test step blocks tag creation — the release is never cut
on a broken build.

## Local equivalents

```bash
# 01-ci quality gate
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run bandit -r src/ -ll
uv run lint-imports
uv run pytest --cov=src/ --cov-report=xml -q

# Local release (never in CI)
uv run build.py
```
