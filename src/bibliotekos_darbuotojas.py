from src.db_base import DBBase
from pradine_info import bibliotekos_darbuotojas_data
from psycopg2 import sql

class BibliotekosDarbuotojas(DBBase):
    def __init__(self):
        super().__init__("bibliotekos_darbuotojas", (
            'vardas', 'pavarde', 'asmens_kodas', 'telefono_numeris', 'el_pastas',
            'darbuotojo_pareigos', 'darbuotojo_atlyginimas'
        ))

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            vardas VARCHAR(255),
            pavarde VARCHAR(255),
            asmens_kodas INT UNIQUE,
            telefono_numeris VARCHAR(50),
            el_pastas VARCHAR(255),
            darbuotojo_pareigos VARCHAR(255),
            darbuotojo_atlyginimas DECIMAL
        )
        """
        super().create_table(query)

    def clear_data(self):
        delete_query = sql.SQL("DELETE FROM {}").format(sql.Identifier(self.table_name))
        self.cursor.execute(delete_query)
        self.connection.commit()
        print(f"Data cleared from {self.table_name}!")

    def insert_data(self, data):
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
        except Exception as e:
            print(f"Klaida įdedant duomenis į {self.table_name}: {e}")
            self.connection.rollback()

    def insert_all_data(self):
        for employee in bibliotekos_darbuotojas_data:
            self.insert_data(employee)

    def select_by_code(self, asmens_kodas):
        query = sql.SQL("SELECT * FROM {} WHERE asmens_kodas = %s").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(query, (asmens_kodas,))
        return self.cursor.fetchone()

    def print_employee(self, asmens_kodas):
        employee = self.select_by_code(asmens_kodas)
        if employee:
            print(f"Bibliotekos darbuotojas:\n"
                  f"Vardas: {employee[1]}\n"
                  f"Pavardė: {employee[2]}\n"
                  f"Asmens kodas: {employee[3]}\n"
                  f"Telefonas: {employee[4]}\n"
                  f"El. paštas: {employee[5]}\n"
                  f"Pareigos: {employee[6]}\n"
                  f"Atlyginimas: {employee[7]}")
        else:
            print("Bibliotekos darbuotojas nerastas.")

    def add_book(self, knyga_data):
        # Implement method to add a book
        from knyga import Knyga
        with Knyga() as knyga:
            knyga.create_table()  # Ensure table exists
            knyga.insert_data(knyga_data)  # Insert the new book
            print("Knyga pridėta.")

    def remove_book_by_name(self, pavadinimas):
        from knyga import Knyga
        with Knyga() as knyga:
            knyga.create_table()  # Ensure table exists
            knyga.remove_book_by_name(pavadinimas)  # Delete the book
            print("Knyga pašalinta.")
