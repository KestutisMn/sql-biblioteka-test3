from src.db_base import DBBase
from pradine_info import knygos_ir_kategorijos_data
from psycopg2 import sql

class KnygosIrKategorijos(DBBase):
    def __init__(self):
        """
        Initializes the KnygosIrKategorijos class, inheriting from DBBase.
        Sets the table name to 'knygos_ir_kategorijos' and defines columns
        representing the relationship between books and categories.
        """
        super().__init__("knygos_ir_kategorijos", ('knygos_id', 'kategorijos_id'))

    def create_table(self):
        """
        Creates the 'knygos_ir_kategorijos' table if it does not already exist.

        The table includes columns for book ID (knygos_id) and category ID
        (kategorijos_id). Both columns are foreign keys referencing the 'knyga'
        and 'knygos_kategorija' tables, respectively. The combination of these
        columns forms a composite primary key.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            knygos_id INTEGER REFERENCES knyga(ID),
            kategorijos_id INTEGER REFERENCES knygos_kategorija(ID),
            PRIMARY KEY (knygos_id, kategorijos_id)
        )
        """
        super().create_table(create_query)

    def insert_all_data(self):
        """
        Inserts all records from knygos_ir_kategorijos_data into the 'knygos_ir_kategorijos' table.

        Iterates through knygos_ir_kategorijos_data and inserts each record into the table.
        If a conflict occurs (e.g., a duplicate book-category pair), the insertion
        is skipped for that record.
        """
        insert_query = sql.SQL("""
        INSERT INTO {table} (knygos_id, kategorijos_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in knygos_ir_kategorijos_data:
            self.cursor.execute(insert_query, data)
        self.connection.commit()  # Commit the transaction

    def select_all(self):
        """
        Retrieves all records from the 'knygos_ir_kategorijos' table.

        Returns:
        list of tuples: A list of all rows in the 'knygos_ir_kategorijos' table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
