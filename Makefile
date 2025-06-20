run:
	docker compose up

gui:
	open http://localhost:7474

cmd:
	@PYTHONPATH=. uv run python app/main.py ${ARG}

format:
	uv run ruff format app
	uv run ruff check app --fix --show-fixes
	uv run mypy app
