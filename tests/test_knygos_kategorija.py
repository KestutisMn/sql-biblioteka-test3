import pytest
from src.knygos_kategorija import KnygosKategorija

@pytest.fixture
def knygos_kategorija():
    instance = KnygosKategorija()
    instance.create_table()
    yield instance
    # Clean up after tests
    instance.drop_table()

def test_insert_and_select(knygos_kategorija):
    knygos_kategorija.insert_all_data()
    results = knygos_kategorija.select_all()
    assert len(results) == 5  # Check number of inserted categories
    # Check if 'Fantasy' is among the results
    assert any(record[1] == 'Fantasy' for record in results)
