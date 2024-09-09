# Library Management System

This program is a library management system that uses a PostgreSQL database. It allows you to create and manage tables, insert and update data about authors, library staff, books, their categories and locations, as well as book loans and visitors.

## Project Structure

1. **`src/db_base.py`**:
   - The main base class `DBBase`, which handles database connections, table creation, and data insertion.

2. **`src/autorius.py`**:
   - The `Author` class, which manages the `authors` table. Supports table creation, data insertion, and querying.

3. **`src/bibliotekos_darbuotojas.py`**:
   - The `LibraryStaff` class, which manages the `library_staff` table. Supports table creation, data insertion, and querying.

4. **`src/knyga.py`**:
   - The `Book` class, which manages the `books` table. Supports table creation, data insertion, and querying.

5. **`src/knygos_ir_kategorijos.py`**:
   - The `BooksAndCategories` class, which manages the `books_and_categories` table. Supports table creation, data insertion, and querying.

6. **`src/knygos_kategorija.py`**:
   - The `BookCategory` class, which manages the `book_category` table. Supports table creation, data insertion, and querying.

7. **`src/knygos_vieta.py`**:
   - The `BookLocation` class, which manages the `book_location` table. Supports table creation, data insertion, and querying.

8. **`src/knygu_skolinimai.py`**:
   - The `BookLoans` class, which manages the `book_loans` table. Supports table creation, data insertion, and querying.

9. **`src/lankytojas.py`**:
   - The `Visitor` class, which manages the `visitors` table. Supports table creation, data insertion, and querying.

10. **`main.py`**:
    - The main executable file that uses the above classes to create tables and insert data into the database.

11. **`pradine_info.py`**:
    - Sample data for tables (`author_data`, `library_staff_data`, `book_data`, `books_and_authors_data`, `books_and_categories_data`, `book_category_data`, `book_location_data`, `book_loans_data`, `visitor_data`).

## Dependencies

This project requires the following Python libraries:
- `psycopg2` – For PostgreSQL database connection.
- `python-dotenv` – For managing environment variables.

## Configuration

Create a `.env` file in the project's root directory with the following parameters:

makefile
#DATABASE_NAME=your_database_name
DB_USERNAME=your_username
PASSWORD=your_password
HOST=your_database_host
PORT=your_database_port

Usage
To run the application, use:
python main.py

To install dependencies, use:
pip install psycopg2-binary python-dotenv

![SQL BIBLIOTEKA 240812.drawio.png](diagrams%2FSQL%20BIBLIOTEKA%20240812.drawio.png)
