import pytest
from src.bibliotekos_darbuotojas import BibliotekosDarbuotojas

@pytest.fixture
def db():
    with BibliotekosDarbuotojas() as darbuotojas:
        yield darbuotojas

def test_create_table(db):
    db.create_table()
    assert db.table_exists()

def test_insert_data(db):
    data = ('John', 'Doe', 12345, '555-0101', 'john.doe@example.com', 'Librarian', 3500)
    db.insert_data(data)
    db.connection.commit()
    db.cursor.execute("SELECT * FROM bibliotekos_darbuotojas WHERE asmens_kodas = %s", (12345,))
    result = db.cursor.fetchone()
    assert result is not None

def test_clear_data(db):
    db.clear_data()
    db.cursor.execute("SELECT COUNT(*) FROM bibliotekos_darbuotojas")
    count = db.cursor.fetchone()[0]
    assert count == 0

def test_insert_all_data(db):
    db.insert_all_data()
    db.cursor.execute("SELECT COUNT(*) FROM bibliotekos_darbuotojas")
    count = db.cursor.fetchone()[0]
    assert count > 0
