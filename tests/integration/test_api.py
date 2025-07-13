import pytest

from chatbot_api.src.utils.async_utils import async_retry
from chatbot_api.src.models.hospital_rag_query import HospitalQueryInput, HospitalQueryOutput


class TestWorkflowIntegration:
    @pytest.mark.asyncio
    async def test_async_retry_with_business_logic(self):
        """Test async_retry works with our business functions."""
        call_count = 0
        
        @async_retry(max_retries=3, delay=0.01)
        async def unreliable_data_processor(input_text):
            nonlocal call_count
            call_count += 1
            
            if call_count < 2:
                raise Exception("Processing failed")
            
            # Our business logic: process input and create output
            query_input = HospitalQueryInput(text=input_text)
            query_output = HospitalQueryOutput(
                input=query_input.text,
                output=f"Processed: {query_input.text}",
                intermediate_steps=[f"Attempt {call_count}", "Success"]
            )
            return query_output

        result = await unreliable_data_processor("Test query")
        
        assert result.input == "Test query"
        assert "Processed: Test query" == result.output
        assert len(result.intermediate_steps) == 2
        assert call_count == 2  # Failed once, succeeded on second try

