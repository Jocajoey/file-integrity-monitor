# File Integrity Monitor (Python)

Detects file changes using cryptographic hashing (SHA‑256).

## Quick start
```bash
python src/fim.py init  <DIR> --db baseline.json
python src/fim.py scan  <DIR> --db baseline.json
python src/fim.py update <DIR> --db baseline.json
