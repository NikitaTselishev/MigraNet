mypy .
black --exclude ./venv -l 79 .
python prepare_database.py
python -m unittest
python drop_database.py