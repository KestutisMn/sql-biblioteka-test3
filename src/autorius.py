from src.db_base import DBBase
from src.pradine_info import autorius_data
from psycopg2 import sql

class Autorius(DBBase):
    def __init__(self):
        """
        Initializes the Autorius class, inheriting from DBBase.
        Sets the table name to 'autorius' and columns to ('vardas', 'pavarde').
        """
        super().__init__("autorius", ('vardas', 'pavarde'))

    def create_table(self):
        """
        Creates the 'autorius' table if it does not already exist.
        The table has columns: id (SERIAL PRIMARY KEY), vardas (VARCHAR(100) NOT NULL),
        and pavarde (VARCHAR(100) NOT NULL).
        """
        create_query = """
        CREATE TABLE IF NOT EXISTS autorius (
            id SERIAL PRIMARY KEY,
            vardas VARCHAR(100) NOT NULL,
            pavarde VARCHAR(100) NOT NULL
        );
        """
        super().create_if_not_exists(create_query)  # Creates the table if it doesn't exist

    def clear_data(self):
        """
        Deletes all records from the 'autorius' table.

        Prints a confirmation message upon successful deletion, or an error message if
        an exception occurs during the process.
        """
        try:
            query = sql.SQL("DELETE FROM {}").format(sql.Identifier(self.table_name))
            self.cursor.execute(query)
            self.connection.commit()
            print(f'Visi duomenys iš {self.table_name} lentelės ištrinti.')
        except Exception as e:
            print(f"Klaida ištrinant duomenis iš {self.table_name}: {e}")
            self.connection.rollback()

    def insert_all_data(self):
        """
        Inserts all data from the autorius_data into the 'autorius' table.

        Iterates through autorius_data and calls insert_data for each record.
        Prints a success message or an error message if an exception occurs.
        """
        try:
            for author in autorius_data:
                self.insert_data(author)
            print(f'Duomenys sėkmingai įrašyti į {self.table_name}.')
        except Exception as e:
            print(f"Klaida įrašant duomenis į {self.table_name}: {e}")
            self.connection.rollback()

    def insert_data(self, data):
        """
        Inserts a single record into the 'autorius' table.

        If a conflict occurs (e.g., the record already exists), the insertion is skipped.
        Prints the query being executed and the data being inserted.

        Parameters:
        data (tuple): The data to be inserted, should match the columns of the table.
        """
        conflict_action = 'DO NOTHING'  # If author already exists, skip the insertion

        query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({})
            ON CONFLICT DO NOTHING
        """).format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(map(sql.Identifier, self.columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(self.columns))
        )

        print(f"Executing query: {query.as_string(self.connection)}")
        print(f"With data: {data}")

        self.cursor.execute(query, data)
        self.connection.commit()

    def select_all(self):
        """
        Retrieves all records from the 'autorius' table.

        Returns:
        list of tuples: A list of all rows in the 'autorius' table.
        """
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name))
        self.cursor.execute(query)
        return self.cursor.fetchall()
