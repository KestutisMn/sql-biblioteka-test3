import pytest
from src.lankytojas import Lankytojas

@pytest.fixture
def lankytojas():
    with Lankytojas() as instance:
        instance.create_table()
        yield instance

def test_insert_and_select(lankytojas):
    lankytojas.insert_all_data()
    results = lankytojas.select_all()
    assert len(results) == 4  # Check number of inserted visitors
    assert ('Alice', 'Brown', 56789, '555-0103', 'alice.brown@example.com', 1, 1, True) in results
