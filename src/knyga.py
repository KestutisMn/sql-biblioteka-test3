from src.db_base import DBBase
from pradine_info import knyga_data
from psycopg2 import sql

class Knyga(DBBase):
    def __init__(self):
        """
        Initializes the Knyga class, inheriting from DBBase.
        Sets the table name to 'knyga' and defines columns related to books.
        """
        columns = (
            'pavadinimas', 'knygos_autorius', 'knygos_statusas',
            'kategorija_id', 'knygos_vieta_id', 'knygos_ivedimo_data',
            'knygos_pasalinimo_data'
        )
        super().__init__('knyga', columns)

    def create_table(self):
        """
        Creates the 'knyga' table if it does not already exist.

        The table includes columns for book details such as title, author, status,
        category, location, entry date, and removal date. Also enforces a uniqueness
        constraint on the book title.

        Foreign key constraints reference the 'autorius', 'knygos_kategorija',
        and 'knygos_vieta' tables.
        """
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            pavadinimas VARCHAR(255),
            knygos_autorius INTEGER REFERENCES autorius(ID) ON DELETE CASCADE,
            knygos_statusas VARCHAR(50),
            kategorija_id INTEGER REFERENCES knygos_kategorija(ID) ON DELETE CASCADE,
            knygos_vieta_id INTEGER REFERENCES knygos_vieta(ID) ON DELETE CASCADE,
            knygos_ivedimo_data DATE,
            knygos_pasalinimo_data DATE,
            UNIQUE (pavadinimas)
        )
        """
        super().create_table(create_query)

    def insert_all_data(self):
        """
        Inserts all records from knyga_data into the 'knyga' table.

        Iterates through knyga_data and inserts each record into the table.
        If a conflict occurs (e.g., a book with the same title already exists),
        the insertion is skipped for that record.
        """
        insert_query = sql.SQL("""
        INSERT INTO {table} (pavadinimas, knygos_autorius, knygos_statusas, kategorija_id, knygos_vieta_id, knygos_ivedimo_data, knygos_pasalinimo_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (pavadinimas) DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in knyga_data:
            self.cursor.execute(insert_query, data)
        self.connection.commit()  # Commit the transaction

    def select_all(self):
        """
        Retrieves all records from the 'knyga' table.

        Returns:
        list of tuples: A list of all rows in the 'knyga' table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def remove_book_by_name(self, pavadinimas):
        # Pašalinti visus skolinimus, susijusius su knyga
        # delete_borrowing_query = sql.SQL(
        #     "DELETE FROM knygu_skolinimai WHERE knyga_id IN (SELECT ID FROM {} WHERE pavadinimas = %s)").format(
        #     sql.Identifier(self.table_name))
        # self.cursor.execute(delete_borrowing_query, (pavadinimas,))

        # Pašalinti knygą
        def remove_book_by_name(self, pavadinimas):
            # Paimame knygos ID pagal pavadinimą
            select_book_query = sql.SQL("SELECT ID FROM {} WHERE pavadinimas = %s").format(
                sql.Identifier(self.table_name))
            self.cursor.execute(select_book_query, (pavadinimas,))
            book_id = self.cursor.fetchone()

            if book_id:
                # Pašaliname knygą pagal ID
                delete_book_query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(self.table_name))
                self.cursor.execute(delete_book_query, (book_id,))
                self.connection.commit()
                print(f"Knyga su pavadinimu '{pavadinimas}' pašalinta.")
            else:
                print(f"Knyga su pavadinimu '{pavadinimas}' nerasta.")
