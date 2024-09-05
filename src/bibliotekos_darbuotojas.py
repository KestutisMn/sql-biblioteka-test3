from src.db_base import DBBase
from pradine_info import bibliotekos_darbuotojas_data
from psycopg2 import sql  # Import for SQL query construction

class BibliotekosDarbuotojas(DBBase):
    def __init__(self):
        """
        Initializes the BibliotekosDarbuotojas class, inheriting from DBBase.
        Sets the table name to 'bibliotekos_darbuotojas' and defines columns
        including personal and employment details.
        """
        super().__init__("bibliotekos_darbuotojas", (
            'vardas', 'pavarde', 'asmens_kodas', 'telefono_numeris', 'el_pastas',
            'darbuotojo_pareigos', 'darbuotojo_atlyginimas'
        ))

    def create_table(self):
        """
        Creates the 'bibliotekos_darbuotojas' table if it does not already exist.

        The table has columns: ID (SERIAL PRIMARY KEY), vardas (VARCHAR(255)),
        pavarde (VARCHAR(255)), asmens_kodas (INT UNIQUE), telefono_numeris
        (VARCHAR(50)), el_pastas (VARCHAR(255)), darbuotojo_pareigos
        (VARCHAR(255)), and darbuotojo_atlyginimas (DECIMAL).
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            vardas VARCHAR(255),
            pavarde VARCHAR(255),
            asmens_kodas INT UNIQUE,  -- UNIQUE constraint added
            telefono_numeris VARCHAR(50),
            el_pastas VARCHAR(255),
            darbuotojo_pareigos VARCHAR(255),
            darbuotojo_atlyginimas DECIMAL
        )
        """
        super().create_table(query)

    def clear_data(self):
        """
        Deletes all records from the 'bibliotekos_darbuotojas' table.

        Prints a confirmation message upon successful deletion.
        """
        delete_query = sql.SQL("DELETE FROM {}").format(sql.Identifier(self.table_name))
        self.cursor.execute(delete_query)
        self.connection.commit()
        print(f"Data cleared from {self.table_name}!")

    def insert_data(self, data):
        """
        Inserts a single record into the 'bibliotekos_darbuotojas' table.

        If a conflict occurs (e.g., a record with the same asmens_kodas already exists),
        the insertion is skipped.

        Parameters:
        data (tuple): A tuple containing the data to be inserted. It should match the
                      columns of the table in order.
        """
        query = sql.SQL("""
            INSERT INTO {} ({}) VALUES ({})
            ON CONFLICT (asmens_kodas) DO NOTHING
        """).format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(map(sql.Identifier, self.columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(self.columns))
        )
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            print(f'Data inserted into {self.table_name}!')
        except Exception as e:
            print(f"Klaida įdedant duomenis į {self.table_name}: {e}")
            self.connection.rollback()

    def insert_all_data(self):
        """
        Inserts all records from bibliotekos_darbuotojas_data into the
        'bibliotekos_darbuotojas' table.

        Iterates through bibliotekos_darbuotojas_data and calls insert_data for each record.
        """
        for employee in bibliotekos_darbuotojas_data:
            self.insert_data(employee)
