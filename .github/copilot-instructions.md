# Copilot Instructions for This Workspace

- Repo state: only `secure.ipynb` exists and it contains no cells yet; there is no code, tests, or environment metadata. Treat this as a greenfield data/notebook project until more files are added.
- Goal when coding: clarify with the user what the notebook is meant to do (analysis, ML training, data prep, security demo, etc.) before creating cells or new modules.

## Working in the notebook
- Add code cells with clear markdown explaining intent; mirror the pattern of keeping notebooks self-contained until a package/module structure is introduced.
- Prefer small, restart-friendly cells: load data, transform, model, evaluate in separate steps; persist intermediate artifacts to disk if reruns are needed.
- If you add outputs (plots/tables), keep rendering lightweight and deterministic; avoid large embedded binaries.

## Project structure and files
- Current files: `secure.ipynb` (empty). Create new notebooks in the repo root unless/until a `notebooks/` folder is introduced. For reusable code, propose creating a `src/` package and refactoring shared logic out of notebooks.
- Data handling: if reading local files, prompt the user for paths and avoid hard-coding secrets; use relative paths under a future `data/` directory when feasible.

## Dependencies and environment
- No `requirements.txt`/`environment.yml` yet. When adding libraries, list them explicitly in a new `requirements.txt` and note exact versions you test with in markdown inside the notebook.
- Use deterministic installs (pin versions) and prefer widely available packages to reduce setup friction.

## Testing and validation
- There are no tests. If you add reusable Python modules, scaffold lightweight unit tests (e.g., `tests/`) and runnable commands (e.g., `python -m pytest tests`). Document any commands you add in this file.
- For notebooks, include quick validation cells (shape checks, null counts, basic assertions) near data-loading steps.

## Security and secrets
- Do not store credentials or tokens in the notebook. If required, use environment variables and remind the user to set them locally; do not commit secrets.
- Scrub outputs before saving if they could leak sensitive data.

## Collaboration hygiene
- Keep cells ordered and runnable top-to-bottom; restart & run all before handing off.
- Add brief inline comments only for non-obvious logic; rely on markdown for high-level rationale.

## Next steps to clarify with the user
- Confirm the notebook’s intended purpose and data sources.
- Ask if a structured project layout (e.g., `notebooks/`, `src/`, `data/`, `tests/`) should be created now.
- Confirm preferred Python version and dependency baseline before introducing packages.
