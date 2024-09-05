from src.db_base import DBBase
from pradine_info import lankytojas_data
from psycopg2 import sql

class Lankytojas(DBBase):
    def __init__(self):
        """
        Initializes the Lankytojas class, inheriting from DBBase.
        Sets the table name to 'lankytojas' and defines columns
        related to visitors, including personal information, contact details,
        book lists, status, and registration information.
        """
        super().__init__("lankytojas", (
            'vardas', 'pavarde', 'asmens_kodas', 'telefono_numeris', 'el_pastas',
            'knygu_sarasas', 'lankytojo_statusas', 'registruotas'
        ))

    def create_table(self):
        """
        Creates the 'lankytojas' table if it does not already exist.

        The table includes columns for visitor's first name (vardas),
        last name (pavarde), personal code (asmens_kodas), contact details
        (telefono_numeris and el_pastas), a list of books (knygu_sarasas),
        visitor status (lankytojo_statusas), and registration status (registruotas).
        A unique constraint is applied to the personal code to ensure no duplicates.
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            vardas VARCHAR(255),
            pavarde VARCHAR(255),
            asmens_kodas BIGINT UNIQUE,
            telefono_numeris VARCHAR(50),
            el_pastas VARCHAR(255),
            knygu_sarasas INT,
            lankytojo_statusas INT,
            registruotas BOOLEAN
        )
        """
        super().create_table(query)

    def insert_all_data(self):
        """
        Inserts all records from lankytojas_data into the 'lankytojas' table.

        Iterates through lankytojas_data and inserts each visitor's information into the table.
        If a conflict occurs (e.g., a duplicate personal code), the insertion is skipped
        for that record.
        """
        insert_query = sql.SQL("""
        INSERT INTO {table} (vardas, pavarde, asmens_kodas, telefono_numeris, el_pastas, knygu_sarasas, lankytojo_statusas, registruotas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (asmens_kodas) DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in lankytojas_data:
            self.cursor.execute(insert_query, data)
        self.connection.commit()  # Commit the transaction
