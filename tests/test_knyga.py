import pytest
from src.knyga import Knyga
from datetime import date



@pytest.fixture
def knyga():
    instance = Knyga()
    instance.create_table()
    yield instance
    # Cleanup: Išvalykite lentelę arba uždarykite ryšį po testų, jei reikia
    # instance.connection.close()


def test_insert_and_select(knyga):
    knyga.insert_all_data()
    results = knyga.select_all()

    # Patikrinkite, ar yra tiksliai 11 įrašų
    assert len(results) == 11, "Įterptų knygų skaičius turi būti 11"

    # Tikėtinas įrašas su datetime.date objektais
    expected_record = (
        1,  # ID generuojamas automatiškai
        "Harry Potter and the Sorcerer's Stone",
        1,
        'Available',
        1,
        1,
        date(1997, 6, 26),
        None
    )

    # Patikrinkite, ar tikėtinas įrašas yra rezultatuose
    assert any(record == expected_record for record in results), \
        f"Įrašas {expected_record} neturi būti rezultatuose"


def test_remove_book_by_name(knyga):
    knyga.insert_all_data()
    knyga.remove_book_by_name('Harry Potter and the Sorcerer\'s Stone')
    results = knyga.select_all()

    # Patikrinkite, ar knyga buvo pašalinta
    assert all(record[1] != 'Harry Potter and the Sorcerer\'s Stone' for record in results), \
        "Knyga su pavadinimu 'Harry Potter and the Sorcerer\'s Stone' turi būti pašalinta"
