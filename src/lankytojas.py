from src.db_base import DBBase
from pradine_info import lankytojas_data
from psycopg2 import sql

class Lankytojas(DBBase):
    def __init__(self):
        super().__init__("lankytojas", (
            'vardas', 'pavarde', 'asmens_kodas', 'telefono_numeris', 'el_pastas',
            'knygu_sarasas', 'lankytojo_statusas', 'registruotas'
        ))

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            ID SERIAL PRIMARY KEY,
            vardas VARCHAR(255),
            pavarde VARCHAR(255),
            asmens_kodas BIGINT UNIQUE,
            telefono_numeris VARCHAR(50),
            el_pastas VARCHAR(255),
            knygu_sarasas INT,
            lankytojo_statusas INT,
            registruotas BOOLEAN
        )
        """
        super().create_table(query)

    def insert_all_data(self):
        insert_query = sql.SQL("""
        INSERT INTO {table} (vardas, pavarde, asmens_kodas, telefono_numeris, el_pastas, knygu_sarasas, lankytojo_statusas, registruotas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (asmens_kodas) DO NOTHING
        """).format(table=sql.Identifier(self.table_name))

        for data in lankytojas_data:
            try:
                self.cursor.execute(insert_query, data)
                self.connection.commit()
            except Exception as e:
                print(f"Klaida įdedant duomenis į {self.table_name}: {e}")
                self.connection.rollback()

    def select_by_code(self, asmens_kodas):
        query = sql.SQL("SELECT * FROM {} WHERE asmens_kodas = %s").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(query, (asmens_kodas,))
        return self.cursor.fetchone()

    def print_visitor(self, asmens_kodas):
        visitor = self.select_by_code(asmens_kodas)
        if visitor:
            print(f"Lankytojas:\n"
                  f"Vardas: {visitor[1]}\n"
                  f"Pavardė: {visitor[2]}\n"
                  f"Asmens kodas: {visitor[3]}\n"
                  f"Telefonas: {visitor[4]}\n"
                  f"El. paštas: {visitor[5]}\n"
                  f"Knygų sąrašas: {visitor[6]}\n"
                  f"Lankytojo statusas: {visitor[7]}\n"
                  f"Registruotas: {visitor[8]}")
        else:
            print("Lankytojas nerastas.")
