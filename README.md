# Healthcare RAG Agent 🤖

A Retrieval-Augmented Generation (RAG) agent designed for healthcare information querying, built with LangChain and Neo4j knowledge graphs.

## Overview

This project implements a healthcare-focused RAG chatbot that leverages LangChain's capabilities for natural language processing and Neo4j's graph database for structured healthcare data storage. The application provides an intuitive interface for querying complex healthcare relationships and information.

Based on Real Python's comprehensive LLM RAG Chatbot [tutorial](https://realpython.com/build-llm-rag-chatbot-with-langchain), this implementation extends the foundational concepts with healthcare-specific data modeling and query optimization.

## Key Features

- **Knowledge Graph Integration**: Utilizes Neo4j for efficient healthcare data relationship mapping
- **RESTful API**: FastAPI-powered backend for scalable interactions
- **Interactive UI**: Streamlit-based user interface for seamless user experience
- **Containerized Deployment**: Docker-based architecture for consistent development and deployment

## Prerequisites

- Docker and Docker Compose
- OpenAI API access
- Neo4j AuraDB instance
- Python 3.8+

## Installation

### 1. Clone the Repository

```bash
git clone [repository-url]
cd healthcare-rag-chatbot
```

### 2. Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

# Neo4j Database Configuration
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>

# Data Source URLs
HOSPITALS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/hospitals.csv
PAYERS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/payers.csv
PHYSICIANS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/physicians.csv
PATIENTS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/patients.csv
VISITS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/visits.csv
REVIEWS_CSV_PATH=https://raw.githubusercontent.com/hfhoffman1144/langchain_neo4j_rag_app/main/data/reviews.csv

# Model Configuration
HOSPITAL_AGENT_MODEL=gpt-3.5-turbo-1106
HOSPITAL_CYPHER_MODEL=gpt-3.5-turbo-1106
HOSPITAL_QA_MODEL=gpt-3.5-turbo-0125

# Service Configuration
CHATBOT_URL=http://host.docker.internal:8000/hospital-rag-agent
```

### 3. Build and Deploy

Ensure your Neo4j AuraDB instance is running, then execute:

```bash
make build
```

## Usage

### Starting the Application

```bash
make start
```

### Stopping the Application

```bash
make stop
```

### Accessing the Services

- **API Documentation**: `http://localhost:8000/docs`
- **User Interface**: `http://localhost:8501`

<img width="1614" alt="Screenshot 2024-03-27 at 19 44 54" src="https://github.com/asanmateu/healthcare-rag-chatbot/assets/62403518/ef6de300-5dbd-41a0-b89f-34fbe94473bf">

## Database Architecture

The application utilizes a graph database structure optimized for healthcare data relationships. Understanding this schema will help formulate effective queries.

### Graph Schema Overview

<img width="500" alt="Screenshot 2024-04-07 at 23 45 47" src="https://github.com/asanmateu/healthcare-rag-chatbot/assets/62403518/4884891c-b715-452b-af37-5fe69b9bad9e">

### Node Properties

The following node types and their properties are available for querying:

<img width="500" alt="Screenshot 2024-04-07 at 23 44 17" src="https://github.com/asanmateu/healthcare-rag-chatbot/assets/62403518/56c976ac-6b27-409b-a4e3-81e1caba70d5">

### Relationship Properties

Relationships between nodes contain additional contextual information:

<img width="500" alt="Screenshot 2024-04-07 at 23 44 57" src="https://github.com/asanmateu/healthcare-rag-chatbot/assets/62403518/f6d8ebe5-e808-4e8e-9a4c-5e15d47fa25e">

## Technical Stack

- **LangChain**: Orchestration framework for LLM applications
- **Neo4j**: Graph database for healthcare data storage
- **FastAPI**: High-performance API framework
- **Streamlit**: Interactive web application framework
- **Docker**: Containerization platform
- **OpenAI GPT-3.5**: Language model for natural language understanding

## Contributing

Contributions are welcome. Please ensure that any pull requests maintain the existing code style and include appropriate documentation updates.

## Acknowledgments

This project builds upon the excellent foundation provided by Real Python's LLM RAG Chatbot tutorial.

