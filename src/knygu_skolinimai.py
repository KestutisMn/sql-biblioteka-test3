from src.db_base import DBBase
from pradine_info import knygu_skolinimai_data
from psycopg2 import sql

class KnyguSkolinimai(DBBase):
    def __init__(self):
        """
        Initializes the KnyguSkolinimai class, inheriting from DBBase.
        Sets the table name to 'knygu_skolinimai' and defines columns
        related to book loans, including book ID, visitor ID, loan and return dates,
        and late fees.
        """
        super().__init__("knygu_skolinimai", (
            'knyga_id', 'lankytojas_id', 'paemimo_data', 'grazinimo_data', 'delspinigiai'
        ))

    def create_table(self):
        """
        Creates the 'knygu_skolinimai' table if it does not already exist.

        The table includes columns for book ID (knyga_id), visitor ID (lankytojas_id),
        loan date (paemimo_data), return date (grazinimo_data), and late fees (delspinigiai).
        It includes a unique constraint on the combination of book ID and visitor ID to
        prevent duplicate entries for the same book-visitor pair.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            knyga_id INTEGER REFERENCES knyga(ID) ON DELETE CASCADE
            lankytojas_id INTEGER REFERENCES lankytojas(ID),
            paemimo_data DATE,
            grazinimo_data DATE,
            delspinigiai DECIMAL,
            UNIQUE (knyga_id, lankytojas_id)
        )
        """
        super().create_table(create_query)

    def insert_all_data(self):
        insert_query = sql.SQL("""
        INSERT INTO {table} (knyga_id, lankytojas_id, paemimo_data, grazinimo_data, delspinigiai)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (knyga_id, lankytojas_id)
        DO UPDATE SET delspinigiai = EXCLUDED.delspinigiai
        """).format(table=sql.Identifier(self.table_name))

        for data in knygu_skolinimai_data:
            self.cursor.execute(insert_query, data)
        self.connection.commit()

    def select_all(self):
        """
        Retrieves all records from the 'knygu_skolinimai' table.

        Returns:
        list of tuples: A list of all rows in the 'knygu_skolinimai' table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
