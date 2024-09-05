from src.db_base import DBBase
from pradine_info import knygos_vieta_data
from psycopg2 import sql

class KnygosVieta(DBBase):
    def __init__(self):
        """
        Initializes the KnygosVieta class, inheriting from DBBase.
        Sets the table name to 'knygos_vieta' and defines a column
        representing the locations where books are stored.
        """
        super().__init__("knygos_vieta", ('vietos_pav',))

    def create_table(self):
        """
        Creates the 'knygos_vieta' table if it does not already exist.

        The table includes a column for location names (vietos_pav)
        with a unique constraint to ensure no duplicate locations are inserted.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            vietos_pav VARCHAR(255) UNIQUE
        )
        """
        super().create_table(create_query)

    def insert_all_data(self):
        """
        Inserts all records from knygos_vieta_data into the 'knygos_vieta' table.

        Iterates through knygos_vieta_data and inserts each location name into the table.
        If a conflict occurs (e.g., a duplicate location name), the insertion is skipped
        for that record.
        """
        insert_query = sql.SQL("""
        INSERT INTO {table} (vietos_pav)
        VALUES (%s)
        ON CONFLICT (vietos_pav) DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in knygos_vieta_data:
            self.cursor.execute(insert_query, (data,))
        self.connection.commit()  # Commit the transaction

    def select_all(self):
        """
        Retrieves all records from the 'knygos_vieta' table.

        Returns:
        list of tuples: A list of all rows in the 'knygos_vieta' table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
