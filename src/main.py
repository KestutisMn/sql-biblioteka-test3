from autorius import Autorius
from bibliotekos_darbuotojas import BibliotekosDarbuotojas
from knyga import Knyga
from knygos_ir_autoriai import KnygosIrAutoriai
from knygos_ir_kategorijos import KnygosIrKategorijos
from knygos_kategorija import KnygosKategorija
from knygos_vieta import KnygosVieta
from knygu_skolinimai import KnyguSkolinimai
from lankytojas import Lankytojas


def main():
    """
    Main function to execute various database operations.

    - Creates and initializes tables for authors, library employees, books,
      book-author relationships, book-category relationships, categories,
      locations, book loans, and visitors.
    - Inserts data into each table if it does not already exist.
    - Fetches and prints all records from each table.
    """

    # Working with the Autorius (Author) table
    with Autorius() as autorius:
        autorius.create_table()  # Create the table if it does not exist
        autorius.insert_all_data()  # Insert data, avoiding duplicates
        all_authors = autorius.select_all()  # Retrieve all authors
        print("All Authors:", all_authors)

    # Working with the BibliotekosDarbuotojas (Library Employee) table
    with BibliotekosDarbuotojas() as darbuotojas:
        darbuotojas.create_table()  # Create the table if it does not exist
        darbuotojas.insert_all_data()  # Insert data, avoiding duplicates
        all_darbuotojai = darbuotojas.select_all()  # Retrieve all library employees
        print("All Library Employees:", all_darbuotojai)

    # Working with the Knyga (Book) table
    with Knyga() as knyga:
        knyga.create_table()  # Create the table if it does not exist
        knyga.insert_all_data()  # Insert data, avoiding duplicates
        all_knygos = knyga.select_all()  # Retrieve all books
        print("All Books:", all_knygos)

    # Working with the KnygosIrAutoriai (Books and Authors) table
    with KnygosIrAutoriai() as knygos_ir_autoriai:
        knygos_ir_autoriai.create_table()  # Create the table if it does not exist
        knygos_ir_autoriai.insert_all_data()  # Insert data, avoiding duplicates
        all_knygos_ir_autoriai = knygos_ir_autoriai.select_all()  # Retrieve all book-author relationships
        print("All Books and Authors:", all_knygos_ir_autoriai)

    # Working with the KnygosIrKategorijos (Books and Categories) table
    with KnygosIrKategorijos() as knygos_ir_kategorijos:
        knygos_ir_kategorijos.create_table()  # Create the table if it does not exist
        knygos_ir_kategorijos.insert_all_data()  # Insert data, avoiding duplicates
        all_knygos_ir_kategorijos = knygos_ir_kategorijos.select_all()  # Retrieve all book-category relationships
        print("All Books and Categories:", all_knygos_ir_kategorijos)

    # Working with the KnygosKategorija (Book Category) table
    with KnygosKategorija() as kategorija:
        kategorija.create_table()  # Create the table if it does not exist
        kategorija.insert_all_data()  # Insert data, avoiding duplicates
        all_kategorijos = kategorija.select_all()  # Retrieve all categories
        print("All Categories:", all_kategorijos)

    # Working with the KnygosVieta (Book Location) table
    with KnygosVieta() as vieta:
        vieta.create_table()  # Create the table if it does not exist
        vieta.insert_all_data()  # Insert data, avoiding duplicates
        all_vietos = vieta.select_all()  # Retrieve all book locations
        print("All Book Locations:", all_vietos)

    # Working with the KnyguSkolinimai (Book Loans) table
    with KnyguSkolinimai() as skolinimai:
        skolinimai.create_table()  # Create the table if it does not exist
        skolinimai.insert_all_data()  # Insert data, updating existing records with new late fees
        all_skolinimai = skolinimai.select_all()  # Retrieve all book loans
        print("All Book Loans:", all_skolinimai)

    # Working with the Lankytojas (Visitor) table
    with Lankytojas() as lankytojas:
        lankytojas.create_table()  # Create the table if it does not exist
        lankytojas.insert_all_data()  # Insert data, avoiding duplicates
        all_lankytojai = lankytojas.select_all()  # Retrieve all visitors
        print("All Visitors:", all_lankytojai)


if __name__ == "__main__":
    main()
