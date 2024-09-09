import pytest
from src.knygu_skolinimai import KnyguSkolinimai

@pytest.fixture
def knygu_skolinimai():
    with KnyguSkolinimai() as instance:
        instance.create_table()
        yield instance

def test_insert_and_select(knygu_skolinimai):
    knygu_skolinimai.insert_all_data()
    results = knygu_skolinimai.select_all()
    assert len(results) == 10  # Check number of inserted rentals
    assert (1, 1, '2024-01-01', '2024-01-15', 0.00) in results
