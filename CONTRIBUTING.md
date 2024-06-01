## setup

### 0. Pre-requesties

- python version manager like pyenv.
- python package manager like uv.

### 1. Creating venv

```bash
uv venv
```

### 2. Installing packages

```bash
uv pip install -r requirements.txt && uv pip install -r dev-requirements.txt
```

## Adding new table to PostgreSQL

### 0. Pre-requesties

- setup postgresql container (run `docker compose up -d` in the project root directory.)
- Installing stocklake (run `uv pip install -e .` in the project root directory.)

### 1. Adding new model of sqlalchemy.

Please modify `stocklake/stores/db/models.py`.

### 2. Generate rivision.

```bash
stocklake database autogenerate-revision --message "Your migration message"
```

### 3. Upgrade database

```bash
stocklake database upgrade
```
