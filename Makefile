
build:
	docker compose up --build

start:
	docker compose up chatbot_api chatbot_frontend

stop:
	docker compose down chatbot_api chatbot_frontend

test:
	uv run pytest tests/ -v --cov=chatbot_api/src --cov=chatbot_frontend/src --cov=hospital_neo4j_etl/src --ignore=tests/performance

test-unit:
	uv run pytest tests/unit/ -v

test-integration:
	uv run pytest tests/integration/ -v

format:
	uv run ruff format chatbot_api/src/ chatbot_frontend/src/ hospital_neo4j_etl/src/ tests/

lint:
	uv run ruff check chatbot_api/src/ chatbot_frontend/src/ hospital_neo4j_etl/src/ tests/

format-check:
	uv run ruff format --check chatbot_api/src/ chatbot_frontend/src/ hospital_neo4j_etl/src/ tests/

lint-fix:
	uv run ruff check --fix chatbot_api/src/ chatbot_frontend/src/ hospital_neo4j_etl/src/ tests/

pre-commit:
	uv run pre-commit run --all-files

install-dev:
	uv pip install -e "chatbot_api[dev]" -e "chatbot_frontend[dev]" -e "hospital_neo4j_etl[dev]"
