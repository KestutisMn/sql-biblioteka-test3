import pytest
from src.autorius import Autorius
from psycopg2 import connect, sql

@pytest.fixture
def db():
    """
    Fixture to create a database connection with the Autorius table.
    The connection is yielded for the tests and closed afterward.
    """
    autorius = Autorius()
    autorius.create_table()  # Ensure the table exists before running tests
    yield autorius
    # Clear the data after tests
    try:
        autorius.clear_data()  # Clear the data after tests
    except AttributeError:
        print("Warning: 'clear_data' method not implemented.")
    # Close the connection if the method exists
    if hasattr(autorius, 'close_connection'):
        autorius.close_connection()

def test_create_table(db):
    """
    Test that checks if the 'autorius' table is successfully created.
    """
    db.create_table()
    db.cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'autorius'
        );
    """)
    table_exists = db.cursor.fetchone()[0]
    assert table_exists is True

def test_insert_data(db):
    """
    Test to insert a single record and verify if it is added to the 'autorius' table.
    """
    data = ('Test', 'Author')
    db.insert_data(data)
    db.connection.commit()  # Ensure the transaction is committed
    db.cursor.execute("SELECT * FROM autorius WHERE vardas = %s AND pavarde = %s", data)
    result = db.cursor.fetchone()
    assert result is not None
    assert result[1] == data[0] and result[2] == data[1]  # Check 'vardas' and 'pavarde'

def test_insert_all_data(db):
    """
    Test to insert all predefined data and check if records were added.
    """
    db.insert_all_data()  # Inserts data from autorius_data
    db.cursor.execute("SELECT COUNT(*) FROM autorius")
    count = db.cursor.fetchone()[0]
    assert count > 0  # Check if data was inserted
