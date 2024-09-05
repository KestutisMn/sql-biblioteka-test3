import pytest
from knygos_kategorija import KnygosKategorija

@pytest.fixture
def knygos_kategorija():
    with KnygosKategorija() as instance:
        instance.create_table()
        yield instance

def test_insert_and_select(knygos_kategorija):
    knygos_kategorija.insert_all_data()
    results = knygos_kategorija.select_all()
    assert len(results) == 5  # Check number of inserted categories
    assert ('Fantasy',) in results
