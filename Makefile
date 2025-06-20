run:
	docker compose up

gui:
	open http://localhost:7474

cmd:
	@PYTHONPATH=. uv run python app/main.py ${ARG}
