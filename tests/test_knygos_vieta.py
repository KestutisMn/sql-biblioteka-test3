import pytest
from knygos_vieta import KnygosVieta

@pytest.fixture
def knygos_vieta():
    with KnygosVieta() as instance:
        instance.create_table()
        yield instance

def test_insert_and_select(knygos_vieta):
    knygos_vieta.insert_all_data()
    results = knygos_vieta.select_all()
    assert len(results) == 5  # Check number of inserted locations
    assert ('Shelf A',) in results
