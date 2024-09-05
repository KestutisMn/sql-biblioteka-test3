import pytest
from knygos_ir_kategorijos import KnygosIrKategorijos

@pytest.fixture
def knygos_ir_kategorijos():
    with KnygosIrKategorijos() as instance:
        instance.create_table()
        yield instance

def test_insert_and_select(knygos_ir_kategorijos):
    knygos_ir_kategorijos.insert_all_data()
    results = knygos_ir_kategorijos.select_all()
    assert len(results) == 10  # Check number of inserted relationships
    assert (1, 1) in results
