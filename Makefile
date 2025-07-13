
build:
	docker compose up --build

start:
	docker compose up chatbot_api chatbot_frontend

stop:
	docker compose down chatbot_api chatbot_frontend

test:
	pytest tests/ -v --cov=chatbot_api/src --cov=chatbot_frontend/src --cov=hospital_neo4j_etl/src

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

format:
	black chatbot_api/src/ chatbot_frontend/src/ hospital_neo4j_etl/src/ tests/
	
lint:
	flake8 chatbot_api/src/ chatbot_frontend/src/ hospital_neo4j_etl/src/ tests/

install-dev:
	uv pip install -e "chatbot_api[dev]" -e "chatbot_frontend[dev]" -e "hospital_neo4j_etl[dev]"

