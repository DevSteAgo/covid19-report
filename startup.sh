

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt


.venv/bin/python scripts/import_data.py
exec .venv/bin/flask --app app run