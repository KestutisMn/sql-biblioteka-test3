import pytest
from src.bibliotekos_darbuotojas import BibliotekosDarbuotojas


@pytest.fixture
def db():
    """
    Fixture to create a database connection with the BibliotekosDarbuotojas table.
    The connection is yielded for the tests and cleared afterward.
    """
    darbuotojas = BibliotekosDarbuotojas()
    darbuotojas.create_table()  # Ensure the table exists before running tests
    yield darbuotojas
    # Clear the data after tests
    try:
        darbuotojas.clear_data()  # Clear the data after tests
    except AttributeError:
        print("Warning: 'clear_data' method not implemented.")
    # Close the connection if the method exists
    if hasattr(darbuotojas, 'close_connection'):
        darbuotojas.close_connection()

def test_create_table(db):
    """
    Test that checks if the 'bibliotekos_darbuotojas' table is successfully created.
    """
    db.create_table()
    db.cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'bibliotekos_darbuotojas'
        );
    """)
    table_exists = db.cursor.fetchone()[0]
    assert table_exists is True

def test_insert_data(db):
    """
    Test to insert a single record and verify if it is added to the 'bibliotekos_darbuotojas' table.
    """
    data = ('John', 'Doe', '12345', '555-0101', 'john.doe@example.com', 'Librarian', 3500)  # Note the quotes around '12345'
    db.insert_data(data)
    db.connection.commit()  # Ensure the transaction is committed
    db.cursor.execute("SELECT * FROM bibliotekos_darbuotojas WHERE asmens_kodas = %s", ('12345',))  # Note the quotes around '12345'
    result = db.cursor.fetchone()
    assert result is not None
    assert result[2] == data[2]  # Check 'asmens_kodas'

def test_clear_data(db):
    """
    Test to clear all data from the 'bibliotekos_darbuotojas' table and verify that it's empty.
    """
    db.clear_data()
    db.cursor.execute("SELECT COUNT(*) FROM bibliotekos_darbuotojas")
    count = db.cursor.fetchone()[0]
    assert count == 0

def test_insert_all_data(db):
    """
    Test to insert all predefined data and check if records were added to the 'bibliotekos_darbuotojas' table.
    """
    db.insert_all_data()
    db.cursor.execute("SELECT COUNT(*) FROM bibliotekos_darbuotojas")
    count = db.cursor.fetchone()[0]
    assert count > 0
