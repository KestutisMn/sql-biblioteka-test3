from src.db_base import DBBase
from pradine_info import knygos_ir_autoriai_data
from psycopg2 import sql

class KnygosIrAutoriai(DBBase):
    def __init__(self):
        """
        Initializes the KnygosIrAutoriai class, inheriting from DBBase.
        Sets the table name to 'knygos_ir_autoriai' and defines columns
        representing book-author relationships.
        """
        super().__init__("knygos_ir_autoriai", ('knygos_id', 'autoriaus_id'))

    def create_table(self):
        """
        Creates the 'knygos_ir_autoriai' table if it does not already exist.

        The table includes columns for book ID (knygos_id) and author ID
        (autoriaus_id). Both columns are foreign keys referencing the 'knyga'
        and 'autorius' tables, respectively. The combination of these columns
        forms a composite primary key.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            knygos_id INTEGER REFERENCES knyga(ID),
            autoriaus_id INTEGER REFERENCES autorius(ID),
            PRIMARY KEY (knygos_id, autoriaus_id)
        )
        """
        super().create_table(create_query)

    def insert_all_data(self):
        """
        Inserts all records from knygos_ir_autoriai_data into the 'knygos_ir_autoriai' table.

        Iterates through knygos_ir_autoriai_data and inserts each record into the table.
        If a conflict occurs (e.g., a duplicate book-author pair), the insertion
        is skipped for that record.
        """
        insert_query = sql.SQL("""
        INSERT INTO {table} (knygos_id, autoriaus_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in knygos_ir_autoriai_data:
            self.cursor.execute(insert_query, data)
        self.connection.commit()  # Commit the transaction

    def select_all(self):
        """
        Retrieves all records from the 'knygos_ir_autoriai' table.

        Returns:
        list of tuples: A list of all rows in the 'knygos_ir_autoriai' table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
