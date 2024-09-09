import pytest
from src.knygos_vieta import KnygosVieta

@pytest.fixture
def knygos_vieta():
    instance = KnygosVieta()
    instance.create_table()
    yield instance
    # Clean up after tests
    instance.drop_table()

def test_insert_and_select(knygos_vieta):
    knygos_vieta.insert_all_data()
    results = knygos_vieta.select_all()
    assert len(results) == 5  # Check number of inserted locations
    # Check if 'Shelf A' is among the results
    assert any(record[1] == 'Shelf A' for record in results)
