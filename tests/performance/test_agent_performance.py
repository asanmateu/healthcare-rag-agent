import pytest
import asyncio
import time
import httpx


class TestAgentPerformance:
    """Performance tests for the hospital RAG agent."""

    @pytest.fixture
    def test_questions(self):
        return [
            "What is the current wait time at Wallace-Hamilton hospital?",
            "Which hospital has the shortest wait time?",
            "At which hospitals are patients complaining about billing and insurance issues?",
            "What is the average duration in days for emergency visits?",
            "What are patients saying about the nursing staff at Castaneda-Hardy?",
            "What was the total billing amount charged to each payer for 2023?",
            "What is the average billing amount for medicaid visits?",
            "How many patients has Dr. Ryan Brown treated?",
            "Which physician has the lowest average visit duration in days?",
            "How many visits are open and what is their average duration in days?",
            "Have any patients complained about noise?",
            "How much was billed for patient 789's stay?",
            "Which physician has billed the most to cigna?",
            "Which state had the largest percent increase in medicaid visits from 2022 to 2023?",
        ]

    @pytest.fixture
    def chatbot_url(self):
        return "http://localhost:8000/hospital-rag-agent"

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_async_performance_benchmark(self, test_questions, chatbot_url):
        """Test async performance of multiple concurrent requests."""

        async def make_request(question: str) -> httpx.Response:
            timeout = httpx.Timeout(timeout=120)
            async with httpx.AsyncClient() as client:
                return await client.post(
                    chatbot_url, json={"text": question}, timeout=timeout
                )

        start_time = time.perf_counter()
        tasks = [make_request(q) for q in test_questions]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.perf_counter()

        total_time = end_time - start_time
        successful_responses = [
            r
            for r in responses
            if isinstance(r, httpx.Response) and r.status_code == 200
        ]

        assert len(successful_responses) > 0, "No successful responses received"
        assert total_time < 300, f"Async requests took too long: {total_time}s"

        print(f"Async performance: {len(test_questions)} requests in {total_time:.2f}s")
        print(
            f"Successful responses: {len(successful_responses)}/{len(test_questions)}"
        )

    @pytest.mark.slow
    def test_sync_performance_benchmark(self, test_questions, chatbot_url):
        """Test synchronous performance for comparison."""
        import requests

        start_time = time.perf_counter()
        responses = []
        for question in test_questions:
            try:
                response = requests.post(
                    chatbot_url, json={"text": question}, timeout=120
                )
                responses.append(response)
            except Exception as e:
                responses.append(e)
        end_time = time.perf_counter()

        total_time = end_time - start_time
        successful_responses = [
            r for r in responses if hasattr(r, "status_code") and r.status_code == 200
        ]

        assert len(successful_responses) > 0, "No successful responses received"

        print(f"Sync performance: {len(test_questions)} requests in {total_time:.2f}s")
        print(
            f"Successful responses: {len(successful_responses)}/{len(test_questions)}"
        )

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_single_request_response_time(self, chatbot_url):
        """Test response time for a single request."""
        question = "What is the current wait time at Wallace-Hamilton hospital?"

        start_time = time.perf_counter()
        timeout = httpx.Timeout(timeout=120)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                chatbot_url, json={"text": question}, timeout=timeout
            )
        end_time = time.perf_counter()

        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 30, f"Single request took too long: {response_time}s"

        print(f"Single request response time: {response_time:.2f}s")
