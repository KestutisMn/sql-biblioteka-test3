import pandas as pd
from autorius import Autorius
from bibliotekos_darbuotojas import BibliotekosDarbuotojas
from knyga import Knyga
from knygos_ir_autoriai import KnygosIrAutoriai
from knygos_ir_kategorijos import KnygosIrKategorijos
from knygos_kategorija import KnygosKategorija
from knygos_vieta import KnygosVieta
from knygu_skolinimai import KnyguSkolinimai
from lankytojas import Lankytojas

def print_all_data():
    """
    Function to fetch and print all data from the database.
    """
    # Working with the Autorius (Author) table
    try:
        with Autorius() as autorius:
            autorius.create_table()
            autorius.insert_all_data()
            all_authors = autorius.select_all()
            authors_df = pd.DataFrame(all_authors, columns=['ID', 'Vardas', 'Pavardė'])
            print("Autorių sąrašas:\n", authors_df)
    except Exception as e:
        print(f"Error fetching authors data: {e}")

    # Working with the BibliotekosDarbuotojas (Library Employee) table
    try:
        with BibliotekosDarbuotojas() as darbuotojas:
            darbuotojas.create_table()
            darbuotojas.insert_all_data()
            all_darbuotojai = darbuotojas.select_all()
            darbuotojai_df = pd.DataFrame(all_darbuotojai, columns=[
                'ID', 'Vardas', 'Pavardė', 'Asmens Kodas', 'Telefono Numeris', 'El. Paštas', 'Pareigos', 'Atlyginimas'
            ])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print("Bibliotekos darbuotojų sąrašas:\n", darbuotojai_df)
    except Exception as e:
        print(f"Error fetching library employees data: {e}")

    # Working with the Knyga (Book) table
    try:
        with Knyga() as knyga:
            knyga.create_table()
            knyga.insert_all_data()
            all_knygos = knyga.select_all()
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            knygos_df = pd.DataFrame(all_knygos, columns=[
                'ID', 'Pavadinimas', 'Autorius_ID', 'Statusas', 'Kategorija_ID', 'Vieta_ID', 'Išdavimo Data',
                'Grąžinimo Data'
            ])
            print("Knygų sąrašas:\n", knygos_df)
    except Exception as e:
        print(f"Error fetching books data: {e}")

    # Working with the KnygosIrAutoriai (Books and Authors) table
    try:
        with KnygosIrAutoriai() as knygos_ir_autoriai:
            knygos_ir_autoriai.create_table()
            knygos_ir_autoriai.insert_all_data()
            all_knygos_ir_autoriai = knygos_ir_autoriai.select_all()
            knygos_ir_autoriai_df = pd.DataFrame(all_knygos_ir_autoriai, columns=['Knygos ID', 'Autoriaus ID'])
            print("Knygų ir autorių sąrašas:\n", knygos_ir_autoriai_df)
    except Exception as e:
        print(f"Error fetching books and authors data: {e}")

    # Working with the KnygosIrKategorijos (Books and Categories) table
    try:
        with KnygosIrKategorijos() as knygos_ir_kategorijos:
            knygos_ir_kategorijos.create_table()
            knygos_ir_kategorijos.insert_all_data()
            all_knygos_ir_kategorijos = knygos_ir_kategorijos.select_all()
            knygos_ir_kategorijos_df = pd.DataFrame(all_knygos_ir_kategorijos, columns=['Knygos ID', 'Kategorijos ID'])
            print("Knygų ir kategorijų sąrašas:\n", knygos_ir_kategorijos_df)
    except Exception as e:
        print(f"Error fetching books and categories data: {e}")

    # Working with the KnygosKategorija (Book Category) table
    try:
        with KnygosKategorija() as kategorija:
            kategorija.create_table()
            kategorija.insert_all_data()
            all_kategorijos = kategorija.select_all()
            kategorijos_df = pd.DataFrame(all_kategorijos, columns=['ID', 'Kategorijos Pavadinimas'])
            print("Kategorijų sąrašas:\n", kategorijos_df)
    except Exception as e:
        print(f"Error fetching categories data: {e}")

    # Working with the KnygosVieta (Book Location) table
    try:
        with KnygosVieta() as vieta:
            vieta.create_table()
            vieta.insert_all_data()
            all_vietos = vieta.select_all()
            vietos_df = pd.DataFrame(all_vietos, columns=['ID', 'Vietos Pavadinimas'])
            print("Knygų vietų sąrašas:\n", vietos_df)
    except Exception as e:
        print(f"Error fetching book locations data: {e}")

    # Working with the KnyguSkolinimai (Book Loans) table
    try:
        with KnyguSkolinimai() as skolinimai:
            skolinimai.create_table()
            skolinimai.insert_all_data()
            all_skolinimai = skolinimai.select_all()
            skolinimai_df = pd.DataFrame(all_skolinimai, columns=[
                'ID', 'Knyga ID', 'Lankytojas ID', 'Paėmimo Data', 'Grąžinimo Data', 'Delspinigiai'
            ])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print("Knygų skolinimų sąrašas:\n", skolinimai_df)
    except Exception as e:
        print(f"Error fetching book loans data: {e}")

    # Working with the Lankytojas (Visitor) table
    try:
        with Lankytojas() as lankytojas:
            lankytojas.create_table()
            lankytojas.insert_all_data()
            all_lankytojai = lankytojas.select_all()
            lankytojas_df = pd.DataFrame(all_lankytojai, columns=[
                'ID', 'Vardas', 'Pavardė', 'Asmens Kodas', 'Telefono Numeris', 'El. Paštas', 'Knygų Sąrašas',
                'Statusas', 'Registruotas'
            ])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print("Lankytojų sąrašas:\n", lankytojas_df)
    except Exception as e:
        print(f"Error fetching visitors data: {e}")

def get_personal_data(asmens_kodas):
    """
    Function to determine if the provided personal code corresponds to a visitor or library employee,
    and then print the associated data.
    """
    # Check if it's a library employee
    try:
        with BibliotekosDarbuotojas() as darbuotojas:
            darbuotojas.create_table()
            darbuotojas.insert_all_data()
            darbuotojas_data = darbuotojas.select_by_code(asmens_kodas)
            if darbuotojas_data:
                darbuotojas_df = pd.DataFrame([darbuotojas_data], columns=[
                    'ID', 'Vardas', 'Pavardė', 'Asmens Kodas', 'Telefono Numeris', 'El. Paštas', 'Pareigos', 'Atlyginimas'
                ])
                print("\nBibliotekos darbuotojo informacija:\n", darbuotojas_df)

                # Allow for book management actions
                action = input("\nAr norite pridėti ar pašalinti knygą? (pridėti/pašalinti): ").strip().lower()
                if action == 'pridėti':
                    pavadinimas = input("Įveskite knygos pavadinimą: ")
                    autorius_id = input("Įveskite autoriaus ID: ")
                    statusas = input("Įveskite knygos statusą: ")
                    kategorija_id = input("Įveskite kategorijos ID: ")
                    vieta_id = input("Įveskite vietos ID: ")
                    ivedimo_data = input("Įveskite įvedimo datą (YYYY-MM-DD): ")
                    pasalinimo_data = input("Įveskite pašalinimo datą (YYYY-MM-DD): ")

                    knyga_data = (
                        pavadinimas, autorius_id, statusas, kategorija_id, vieta_id, ivedimo_data, pasalinimo_data
                    )
                    darbuotojas.add_book(knyga_data)
                elif action == 'pašalinti':
                    pavadinimas = input("Įveskite knygos pavadinimą, kurį norite pašalinti: ")
                    darbuotojas.remove_book_by_name(pavadinimas)
                else:
                    print("Nežinomas veiksmas.")
            else:
                print("Bibliotekos darbuotojas nerastas.")
    except Exception as e:
        print(f"Klaida: {e}")

    # Check if it's a visitor
    try:
        with Lankytojas() as lankytojas:
            lankytojas.create_table()
            lankytojas.insert_all_data()
            lankytojas_data = lankytojas.select_by_code(asmens_kodas)
            if lankytojas_data:
                lankytojas_df = pd.DataFrame([lankytojas_data], columns=[
                    'ID', 'Vardas', 'Pavardė', 'Asmens Kodas', 'Telefono Numeris', 'El. Paštas', 'Knygų Sąrašas',
                    'Statusas', 'Registruotas'
                ])
                print("\nLankytojo informacija:\n", lankytojas_df)
                return
    except Exception as e:
        print(f"Error fetching visitor data: {e}")

    # If no match found
    print("\nAsmuo su įvestu asmens kodu nerastas.")

def main():
    """
    Main function to execute various database operations.

    - Prints all records from each table.
    - Requests the user to input a personal code.
    - Fetches and prints the corresponding data for a visitor or employee.
    """
    # Step 1: Print all data
    print_all_data()

    # Step 2: Ask for personal code
    asmens_kodas = input("\nĮveskite asmens kodą, kad sužinotumėte ar tai lankytojas ar darbuotojas: ")

    # Step 3: Find and print personal data
    get_personal_data(asmens_kodas)

if __name__ == "__main__":
    main()
