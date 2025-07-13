import pytest
from unittest.mock import patch

from chatbot_api.src.utils.async_utils import async_retry


class TestAsyncRetry:
    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        @async_retry(max_retries=3, delay=0.1)
        async def successful_function():
            return "success"

        result = await successful_function()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_success_after_retries(self):
        call_count = 0

        @async_retry(max_retries=3, delay=0.1)
        async def function_with_retries():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"

        result = await function_with_retries()
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_failure_after_max_retries(self):
        call_count = 0

        @async_retry(max_retries=2, delay=0.1)
        async def always_failing_function():
            nonlocal call_count
            call_count += 1
            raise Exception("Always fails")

        with pytest.raises(ValueError, match="Failed after 2 attempts"):
            await always_failing_function()
        
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_custom_delay(self):
        call_count = 0

        @async_retry(max_retries=2, delay=0.01)
        async def function_with_custom_delay():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("First failure")
            return "success"

        with patch('asyncio.sleep') as mock_sleep:
            result = await function_with_custom_delay()
            assert result == "success"
            mock_sleep.assert_called_once_with(0.01)

    @pytest.mark.asyncio
    async def test_preserves_function_args_and_kwargs(self):
        @async_retry(max_retries=1, delay=0.1)
        async def function_with_args(arg1, arg2, kwarg1=None):
            return f"{arg1}-{arg2}-{kwarg1}"

        result = await function_with_args("a", "b", kwarg1="c")
        assert result == "a-b-c"