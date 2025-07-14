import pytest
import os
from unittest.mock import Mock, AsyncMock
from typing import Generator


@pytest.fixture(scope="session")
def test_env() -> Generator[None, None, None]:
    os.environ["ENVIRONMENT"] = "test"
    os.environ["NEO4J_URI"] = "neo4j://localhost:7687"
    os.environ["NEO4J_USERNAME"] = "test"
    os.environ["NEO4J_PASSWORD"] = "test"
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["HOSPITAL_AGENT_MODEL"] = "gpt-3.5-turbo"
    os.environ["HOSPITAL_CYPHER_MODEL"] = "gpt-3.5-turbo"
    os.environ["HOSPITAL_QA_MODEL"] = "gpt-3.5-turbo"
    yield


@pytest.fixture
def mock_neo4j_graph():
    mock_graph = Mock()
    mock_graph.query.return_value = []
    mock_graph.refresh_schema.return_value = None
    return mock_graph


@pytest.fixture
def mock_openai_client():
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content="Test response"))]
    )
    return mock_client


@pytest.fixture
def sample_hospital_data():
    return [{"hospital_name": "Test Hospital"}, {"hospital_name": "Another Hospital"}]


@pytest.fixture
def sample_query_input():
    return {"text": "What is the current wait time at Test Hospital?"}


@pytest.fixture
def sample_agent_response():
    return {
        "input": "Test query",
        "output": "Test response",
        "intermediate_steps": ["Step 1", "Step 2"],
    }
