from unittest.mock import Mock

from hospital_neo4j_etl.src.hospital_bulk_csv_write import _set_uniqueness_constraints, NODES


class TestSetUniquenessConstraints:
    def test_generates_correct_constraint_query(self):
        """Test our constraint query generation logic."""
        mock_tx = Mock()
        
        _set_uniqueness_constraints(mock_tx, "Hospital")
        
        expected_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Hospital)\n        REQUIRE n.id IS UNIQUE;"
        mock_tx.run.assert_called_once_with(expected_query, {})

    def test_works_with_all_defined_node_types(self):
        """Test constraint generation works for all our node types."""
        mock_tx = Mock()
        
        for node in NODES:
            mock_tx.reset_mock()
            _set_uniqueness_constraints(mock_tx, node)
            
            call_args = mock_tx.run.call_args[0]
            query = call_args[0]
            
            assert f"FOR (n:{node})" in query
            assert "REQUIRE n.id IS UNIQUE" in query