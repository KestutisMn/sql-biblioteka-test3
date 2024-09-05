import pytest
from src.autorius import Autorius
from psycopg2 import connect, sql

@pytest.fixture
def db():
    with Autorius() as autorius:
        yield autorius

def test_create_table(db):
    db.create_table()
    assert db.table_exists()  # Assuming this method checks if the table exists

def test_insert_data(db):
    data = ('Test', 'Author')
    db.insert_data(data)
    db.connection.commit()
    db.cursor.execute("SELECT * FROM autorius WHERE vardas = %s AND pavarde = %s", data)
    result = db.cursor.fetchone()
    assert result is not None

def test_clear_data(db):
    db.clear_data()
    db.cursor.execute("SELECT COUNT(*) FROM autorius")
    count = db.cursor.fetchone()[0]
    assert count == 0

def test_insert_all_data(db):
    db.insert_all_data()
    db.cursor.execute("SELECT COUNT(*) FROM autorius")
    count = db.cursor.fetchone()[0]
    assert count > 0  # Check if data was inserted
