# Linting Foundations

1. **Ruff** — formatting + lint + auto-fix (fast).
2. **mypy** — static types (correctness).
   Order matters: first make code *consistent* (Ruff), then make it *correct* (mypy).

---

# A) Ruff (format • check • fix)

## Install

```bash
python -m pip install --upgrade ruff
```

## `pyproject.toml` (put at project root)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
# If your code isn't under src/tests, Ruff still works because we run it on "."
src = ["src", "tests"]
extend-exclude = ["build", "dist", ".venv", ".mypy_cache", ".pytest_cache"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true
docstring-code-line-length = "dynamic"

[tool.ruff.lint]
# A tight set that catches real issues and auto-fixes a lot
select = [
  "E",   # pycodestyle (layout & whitespace)
  "F",   # pyflakes (errors: unused vars/imports, undefined names)
  "I",   # isort (import order)
  "UP",  # pyupgrade (modern syntax, f-strings, etc.)
  "B",   # bugbear (common bugs)
  "C4",  # comprehensions (clearer loops)
  "SIM", # simplify (simpler conditionals/expressions)
  "RUF"  # ruff-specific improvements
]

[tool.ruff.lint.isort]
known-first-party = ["your_package_name"]
combine-as-imports = true
force-sort-within-sections = true
```

### What each line means

* `[tool.ruff]` — start of Ruff config.
* `line-length = 100` — wrap lines at 100 chars (formatter and some lint rules use this).
* `target-version = "py311"` — enables Python-3.11-aware checks/fixes.
* `src = ["src", "tests"]` — where your *first-party* code usually lives (import sorter uses this).
* `extend-exclude = [...]` — folders Ruff should ignore (build artifacts, virtual envs, caches).
* `[tool.ruff.format]` — settings for the formatter (Ruff’s Black-compatible formatter).
* `quote-style = "double"` — normalize strings to double quotes.
* `indent-style = "space"` — use spaces for indentation.
* `docstring-code-format = true` — format code blocks *inside* docstrings.
* `docstring-code-line-length = "dynamic"` — wrap code in docstrings to available width.
* `[tool.ruff.lint]` — enable rule families to lint and auto-fix.
* `select = [...]` — which rule groups to enforce (see comments in the TOML).
* `[tool.ruff.lint.isort]` — options for import sorting.
* `known-first-party` — your package name(s), so imports from it stay in the “first-party” section.
* `combine-as-imports = true` — collapse multiple `as` imports.
* `force-sort-within-sections = true` — strict ordering *within* each import section.

### Commands (what each does)

* `ruff format .` → **format** only (spacing, quotes, wrapping). No linting decisions, no code movement except formatting.
* `ruff check .` → **check** only (reports lint violations; exit non-zero if any). No changes to files.
* `ruff check --fix .` → **fix** what can be auto-fixed (unused imports, import order, many style/safety rules). Might still leave non-fixable findings to address manually.

## `Makefile`

```make
# Simple local automation (no Git/CI)
RUFF ?= ruff

.PHONY: ruff-fix ruff-check ruff-format ruff-clean

ruff-format:
	$(RUFF) format .

ruff-check:
	$(RUFF) check .

# One-shot: autofix lint issues, then format
ruff-fix:
	$(RUFF) check --fix .
	$(RUFF) format .

ruff-clean:
	$(RUFF) clean
```

## Use

```bash
make ruff-fix    # fix imports, spacing, unused vars/imports, modernize, then format
make ruff-check  # only report issues
make ruff-format # only format
```

---

# B) mypy (types = correctness)

## Install

```bash
python -m pip install --upgrade mypy
# add type stubs later as needed, e.g.:
# python -m pip install types-requests types-PyYAML
```

## `pyproject.toml` additions

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_configs = true
warn_return_any = true
warn_redundant_casts = true
warn_unused_ignores = true
no_implicit_optional = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
show_error_codes = true
pretty = true

[mypy-tests.*]
disallow_untyped_defs = false
```

### What each line means

* `[tool.mypy]` — start of mypy config.
* `python_version = "3.11"` — type-check in a 3.11 context.
* `strict = true` — turn on a curated set of safety flags (good defaults).
* `warn_unused_configs = true` — catch typos/unused mypy options.
* `warn_return_any = true` — flag functions that effectively return `Any`.
* `warn_redundant_casts = true` — unnecessary `cast()` calls are flagged.
* `warn_unused_ignores = true` — `# type: ignore` is flagged if it isn’t needed.
* `no_implicit_optional = true` — `Optional[T]` must be written explicitly, not implied by `= None`.
* `disallow_untyped_defs = true` — every function must be annotated.
* `disallow_incomplete_defs = true` — parameters/returns must be fully annotated (no partials).
* `check_untyped_defs = true` — even untyped functions get basic checking of their bodies.
* `show_error_codes = true` — print e.g. `[arg-type]`, helpful for searching docs.
* `pretty = true` — nicer error display.
* `[mypy-tests.*]` — per-module overrides for test code.
* `disallow_untyped_defs = false` — allow looser typing in test modules.

## Makefile targets (append)

```make
MYPY ?= mypy

.PHONY: mypy typecheck qa

mypy:
	$(MYPY) .

typecheck: mypy
qa: ruff-fix mypy
```

---

# C) A short note on `from __future__ import annotations`

Place this at the top of new modules:

```python
from __future__ import annotations
```

**Why it helps**

* **Forward references**: you can reference classes not yet defined in the file (`def f(x: Node): ...` where `Node` is defined later).
* **Lower import overhead**: annotations are stored as *strings* and evaluated only when needed (e.g., by `typing.get_type_hints`), reducing import-time costs and avoiding some circular import issues.
* **Cleaner annotations**: you can write `list[str]` without importing `from __future__ import annotations` on older 3.x; with it, annotations are uniformly modern.

This is still useful on Python 3.11/3.12, and remains a safe default for new code.

---

# D) Everyday Python rules — simplified (with bio examples)

1. **Don’t use mutable defaults**
   Use `None` and create inside.

   ```python
   def collect(gene: str, acc: list[str] | None = None) -> list[str]:
       acc = [] if acc is None else acc
       acc.append(gene)
       return acc
   ```

2. **Catch specific errors**
   Prefer narrow exceptions; keep the traceback when you re-raise.

   ```python
   try:
       count = int(row["reads"])
   except KeyError as e:
       raise KeyError("CSV missing 'reads' column") from e
   except ValueError as e:
       raise ValueError(f"Bad integer: {row['reads']}") from e
   ```

3. **Always close resources (use `with`)**
   Files, network sessions, locks.

   ```python
   from pathlib import Path
   p = Path("samples.csv")
   with p.open(encoding="utf-8") as fh:
       for line in fh: ...
   ```

4. **Equality vs. identity**
   `==` compares values; `is` is only for singletons (`None`).

   ```python
   if sample is None: return
   if status == "PASS": ...
   ```

5. **Don’t shadow builtins**
   Avoid names like `list`, `sum`, `id`.

   ```python
   genes: list[str] = []     # ✓
   # list = []               # ✗
   ```

6. **Pandas: avoid chained assignment—use `.loc` and explicit copies**
   Prevent silent bugs when filtering/assigning.

   ```python
   # ✗ Risky (chained assignment)
   df[df.tpm > 1]["status"] = "EXPRESSED"

   # ✓ Safe: use .loc; copy when slicing
   expressed = df.loc[df["tpm"] > 1].copy()
   expressed.loc[:, "status"] = "EXPRESSED"
   df.loc[df["tpm"] <= 1, "status"] = "LOW"
   ```

7. **Work with large data in chunks/streams**
   Avoid loading everything into memory.

   ```python
   import pandas as pd

   total = 0
   for chunk in pd.read_csv("counts.tsv", sep="\t", chunksize=200_000, dtype={"gene": "string", "count": "Int64"}):
       total += (chunk["count"] > 0).sum()
   print("nonzero rows:", total)
   ```

   Or stream text (incl. gz) line-by-line:

   ```python
   import gzip, io
   def open_text(path: str):
       return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "rt", encoding="utf-8")

   with open_text("reads.fastq.gz") as f:
       for i, line in enumerate(f):
           ...
   ```

8. **Compare floats safely** (expression levels, probabilities)

   ```python
   from math import isclose
   if isclose(tpm, 0.0, abs_tol=1e-9): ...
   ```

9. **Use logging, not `print`, in libraries/pipelines**

   ```python
   import logging
   log = logging.getLogger(__name__)
   log.info("Loaded %d samples", len(samples))
   ```

10. **Subprocess safety** (e.g., `samtools`, `bcftools`)
    Avoid `shell=True` unless necessary; pass a list of args.

    ```python
    import subprocess as sp
    sp.run(["samtools", "view", "-b", "in.sam", "-o", "out.bam"], check=True)
    ```

---

# E) Naming, hardcoding, and imports

**Functions & variables**: `snake_case` — `def load_config()`, `total_count`.
**Classes & exceptions**: `PascalCase` — `class FastQueue:`, `class ParseError(Exception):`.
**Constants**: `UPPER_SNAKE` — `DEFAULT_TIMEOUT = 5`.
**Module/package names**: short, lowercase, no dashes — `mypackage`, `utils.py`.
**Privacy**: leading underscore for internal helpers — `_serialize_user()`.
**No hardcoding**: avoid magic numbers/strings inside logic. Put them as **named constants** or in config/env.
**Imports (order)**:

1. standard library,
2. third-party,
3. first-party (your package).
   Ruff’s `I` rules enforce this automatically.

---

# F) What Ruff actually flags (examples help understanding)

**Five “A-series” (builtins shadowing) rules**
*(Names may vary by Ruff version; examples show the intent.)*

* **A001** variable shadows builtin

  ```python
  list = [1, 2, 3]        # ✗; use "items" instead
  ```
* **A002** argument shadows builtin

  ```python
  def func(id: int): ...   # ✗; use "user_id"
  ```
* **A003** attribute shadows builtin

  ```python
  class T: def __init__(self): self.id = 1  # ✗; "obj_id"
  ```
* **A004/A005** shadowing builtin at class level / global scope (variants)

  ```python
  class Map: pass          # ✗; shadows "map"; prefer "Mapper"
  ```

**Other high-value Ruff rules you enabled**

* **F401** — unused import (auto-removable).
* **F841** — assigned but unused variable.
* **UP** — modernize: e.g., `open(..., encoding="utf-8")`, f-strings, `typing` simplifications.
* **B006** — mutable default argument detected.
* **SIM**/**C4** — simplify boolean logic and prefer comprehensions.

---

# G) What mypy errors look like (and what they mean)

Common codes (you’ll see these with `show_error_codes = true`):

* **[arg-type]** — passing the wrong type to a function.
* **[return-value]** — function returns the wrong type.
* **[assignment]** — assigning a value to a variable of incompatible type.
* **[call-arg]** — wrong number or types of arguments in a call.
* **[attr-defined]** — using an attribute that doesn’t exist on the type.
* **[name-defined]** — name used before definition (or in wrong scope).
* **[index]**/**[operator]** — unsupported indexing or operator usage for a type.

Fix the code or the annotations; avoid `# type: ignore` unless you have a precise justification (and prefer `# type: ignore[code]`).

---

# H) Core PEPs (what to learn and how tools help)

* **PEP 8 — Style Guide**
  Naming, whitespace, imports, line length. *Ruff enforces this automatically (E, I).*
* **PEP 257 — Docstrings**
  One-line summary, details, arguments, returns, exceptions. Keep them accurate and brief.
* **PEP 20 — The Zen of Python**
  Run `python -c "import this"`. Use it as design guidance: “Explicit is better than implicit”, “Simple is better than complex”, etc.
* **PEP 484/526/544 — Typing, variable annotations, protocols**
  Annotate public functions. Prefer **Protocols** (structural typing) to hard dependencies on concrete classes for better testability and layering.

---

# I) Daily workflow

1. Edit code.
2. `make ruff-fix` (get the code clean and auto-fixed).
3. `make typecheck` (prove types are correct).

If something fails, fix the cause. Keep config minimal and consistent.

---

# J) What to add next (in order of impact)

* **Testing**: `pytest` with a small, fast suite; add coverage later.
* **Security**: `bandit` (code checks), `pip-audit` (dependency CVEs).
* **Alternative typing**: Pyright in the editor (catches some issues mypy won’t).
* **Docs**: `docformatter` if you want consistent docstring wrapping.
* **Dead code report**: `vulture` (review findings before removal).
* **Non-Python formatting**: Prettier (md/json/yaml), `shfmt` (shell), `taplo fmt` (TOML).

