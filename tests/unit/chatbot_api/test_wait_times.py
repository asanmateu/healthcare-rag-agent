import pytest
from unittest.mock import patch, Mock

from chatbot_api.src.tools.wait_times import (
    _get_current_hospitals,
    _get_current_wait_time_minutes,
    get_current_wait_times,
    get_most_available_hospital,
)


class TestGetCurrentHospitals:
    @patch("chatbot_api.src.tools.wait_times.Neo4jGraph")
    def test_returns_hospital_names(self, mock_neo4j_graph):
        mock_graph_instance = Mock()
        mock_graph_instance.query.return_value = [
            {"hospital_name": "Hospital A"},
            {"hospital_name": "Hospital B"},
        ]
        mock_neo4j_graph.return_value = mock_graph_instance

        result = _get_current_hospitals()

        assert result == ["hospital a", "hospital b"]
        mock_graph_instance.query.assert_called_once()

    @patch("chatbot_api.src.tools.wait_times.Neo4jGraph")
    def test_handles_empty_result(self, mock_neo4j_graph):
        mock_graph_instance = Mock()
        mock_graph_instance.query.return_value = []
        mock_neo4j_graph.return_value = mock_graph_instance

        result = _get_current_hospitals()

        assert result == []


class TestGetCurrentWaitTimeMinutes:
    @patch("chatbot_api.src.tools.wait_times._get_current_hospitals")
    @patch("tools.wait_times.np.random.randint")
    def test_returns_wait_time_for_valid_hospital(
        self, mock_randint, mock_get_hospitals
    ):
        mock_get_hospitals.return_value = ["test hospital", "another hospital"]
        mock_randint.return_value = 45

        result = _get_current_wait_time_minutes("Test Hospital")

        assert result == 45
        mock_randint.assert_called_once_with(low=0, high=600)

    @patch("chatbot_api.src.tools.wait_times._get_current_hospitals")
    def test_returns_negative_one_for_invalid_hospital(self, mock_get_hospitals):
        mock_get_hospitals.return_value = ["test hospital", "another hospital"]

        result = _get_current_wait_time_minutes("Nonexistent Hospital")

        assert result == -1

    @patch("chatbot_api.src.tools.wait_times._get_current_hospitals")
    @patch("tools.wait_times.np.random.randint")
    def test_case_insensitive_hospital_matching(self, mock_randint, mock_get_hospitals):
        mock_get_hospitals.return_value = ["test hospital"]
        mock_randint.return_value = 30

        result = _get_current_wait_time_minutes("TEST HOSPITAL")

        assert result == 30


class TestGetCurrentWaitTimes:
    @patch("chatbot_api.src.tools.wait_times._get_current_wait_time_minutes")
    def test_formats_wait_time_minutes_only(self, mock_get_wait_time):
        mock_get_wait_time.return_value = 45

        result = get_current_wait_times("Test Hospital")

        assert result == "45 minutes"

    @patch("chatbot_api.src.tools.wait_times._get_current_wait_time_minutes")
    def test_formats_wait_time_hours_and_minutes(self, mock_get_wait_time):
        mock_get_wait_time.return_value = 125  # 2 hours 5 minutes

        result = get_current_wait_times("Test Hospital")

        assert result == "2 hours 5 minutes"

    @patch("chatbot_api.src.tools.wait_times._get_current_wait_time_minutes")
    def test_formats_wait_time_exact_hours(self, mock_get_wait_time):
        mock_get_wait_time.return_value = 120  # 2 hours 0 minutes

        result = get_current_wait_times("Test Hospital")

        assert result == "2 hours 0 minutes"

    @patch("chatbot_api.src.tools.wait_times._get_current_wait_time_minutes")
    def test_handles_nonexistent_hospital(self, mock_get_wait_time):
        mock_get_wait_time.return_value = -1

        result = get_current_wait_times("Nonexistent Hospital")

        assert result == "Hospital 'Nonexistent Hospital' does not exist."


class TestGetMostAvailableHospital:
    @patch("chatbot_api.src.tools.wait_times._get_current_hospitals")
    @patch("chatbot_api.src.tools.wait_times._get_current_wait_time_minutes")
    def test_returns_hospital_with_shortest_wait(
        self, mock_get_wait_time, mock_get_hospitals
    ):
        mock_get_hospitals.return_value = ["hospital a", "hospital b", "hospital c"]
        mock_get_wait_time.side_effect = [60, 30, 45]  # hospital b has shortest wait

        result = get_most_available_hospital(None)

        assert result == {"hospital b": 30}

    @patch("chatbot_api.src.tools.wait_times._get_current_hospitals")
    @patch("chatbot_api.src.tools.wait_times._get_current_wait_time_minutes")
    def test_handles_single_hospital(self, mock_get_wait_time, mock_get_hospitals):
        mock_get_hospitals.return_value = ["only hospital"]
        mock_get_wait_time.return_value = 90

        result = get_most_available_hospital(None)

        assert result == {"only hospital": 90}

    @patch("chatbot_api.src.tools.wait_times._get_current_hospitals")
    def test_handles_no_hospitals(self, mock_get_hospitals):
        mock_get_hospitals.return_value = []

        with pytest.raises(ValueError):
            get_most_available_hospital(None)
