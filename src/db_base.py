import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os


class DBBase:
    def __init__(self, table_name, columns):
        """
        Initializes the DBBase class with database connection and table metadata.

        Parameters:
        table_name (str): The name of the database table.
        columns (tuple): A tuple of column names for the table.
        """
        load_dotenv()
        self.table_name = table_name
        self.columns = columns
        self.connection = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT')
        )
        self.cursor = self.connection.cursor()

    def __enter__(self):
        """
        Allows the use of DBBase class in a 'with' statement for proper resource management.

        Returns:
        DBBase: The current instance of the class.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database cursor and connection upon exiting the 'with' statement.

        Parameters:
        exc_type (type): The type of the exception (if any).
        exc_val (Exception): The exception instance (if any).
        exc_tb (traceback): The traceback object (if any).
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_table(self, create_query):
        """
        Creates a table in the database using the provided SQL query.

        Parameters:
        create_query (str): The SQL query to create the table.
        """
        try:
            self.cursor.execute(create_query)
            self.connection.commit()
            print(f'Lentelė {self.table_name} sukurta arba jau egzistuoja!')
        except Exception as e:
            print(f"Klaida kuriant lentelę {self.table_name}: {e}")
            self.connection.rollback()

    def table_exists(self):
        """
        Checks if the table exists in the database.

        Returns:
        bool: True if the table exists, False otherwise.
        """
        query = sql.SQL("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)")
        self.cursor.execute(query, (self.table_name,))
        return self.cursor.fetchone()[0]

    def create_if_not_exists(self, create_query):
        """
        Creates the table if it does not already exist.

        Parameters:
        create_query (str): The SQL query to create the table.
        """
        if not self.table_exists():
            self.create_table(create_query)
        else:
            print(f'Lentelė {self.table_name} jau egzistuoja, kurti nereikia.')

    def insert_data(self, data, conflict_action='DO NOTHING'):
        """
        Inserts data into the table. If a conflict occurs based on the unique column,
        handles it according to the specified conflict action.

        Parameters:
        data (tuple or list of tuples): The data to be inserted into the table.
                                        Each tuple should match the columns of the table.
        conflict_action (str): The action to take in case of conflict. Defaults to 'DO NOTHING'.
        """
        conflict_column = self.columns[0]  # Assuming the first column is unique

        query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({})
            ON CONFLICT ({})
            {}
        """).format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(map(sql.Identifier, self.columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(self.columns)),
            sql.Identifier(conflict_column),
            sql.SQL(conflict_action)
        )

        try:
            if not isinstance(data[0], tuple):
                data = (data,)
            self.cursor.executemany(query, data)
            self.connection.commit()
            print(f'Įdėti arba atnaujinti duomenys į {self.table_name}!')
        except Exception as e:
            print(f"Klaida įdedant duomenis į {self.table_name}: {e}")
            self.connection.rollback()

    def select_all(self):
        """
        Retrieves all records from the table.

        Returns:
        list of tuples: A list of all rows in the table.
        """
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name))
        self.cursor.execute(query)
        return self.cursor.fetchall()
