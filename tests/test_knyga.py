import pytest
from knyga import Knyga

@pytest.fixture
def knyga():
    with Knyga() as instance:
        instance.create_table()
        yield instance

def test_insert_and_select(knyga):
    knyga.insert_all_data()
    results = knyga.select_all()
    assert len(results) == 10  # Check number of inserted books
    assert ('Harry Potter and the Sorcerer\'s Stone', 1, 'Available', 1, 1, '1997-06-26', None) in results
