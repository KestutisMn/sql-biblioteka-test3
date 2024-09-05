from src.db_base import DBBase
from pradine_info import knygos_kategorija_data
from psycopg2 import sql

class KnygosKategorija(DBBase):
    def __init__(self):
        """
        Initializes the KnygosKategorija class, inheriting from DBBase.
        Sets the table name to 'knygos_kategorija' and defines a column
        representing book categories.
        """
        super().__init__("knygos_kategorija", ('kategorijos_pav',))

    def create_table(self):
        """
        Creates the 'knygos_kategorija' table if it does not already exist.

        The table includes a column for category names (kategorijos_pav)
        with a unique constraint to ensure no duplicate categories are inserted.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            kategorijos_pav VARCHAR(255) UNIQUE
        )
        """
        super().create_table(create_query)

    def insert_all_data(self):
        """
        Inserts all records from knygos_kategorija_data into the 'knygos_kategorija' table.

        Iterates through knygos_kategorija_data and inserts each category name into the table.
        If a conflict occurs (e.g., a duplicate category name), the insertion is skipped
        for that record.
        """
        insert_query = sql.SQL("""
        INSERT INTO {table} (kategorijos_pav)
        VALUES (%s)
        ON CONFLICT (kategorijos_pav) DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in knygos_kategorija_data:
            self.cursor.execute(insert_query, (data,))
        self.connection.commit()  # Commit the transaction

    def select_all(self):
        """
        Retrieves all records from the 'knygos_kategorija' table.

        Returns:
        list of tuples: A list of all rows in the 'knygos_kategorija' table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
