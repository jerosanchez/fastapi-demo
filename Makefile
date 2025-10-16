run:
	bash -c "source .venv/bin/activate && fastapi dev app/main.py"

install:
	bash -c "source .venv/bin/activate && pip install -r requirements.txt"

freeze:
	bash -c "source .venv/bin/activate && pip freeze > requirements.txt"

.PHONY: run install freeze
