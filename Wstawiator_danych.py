import mysql.connector
import pandas as pd
import pathlib as path

con = mysql.connector.connect(
    host = "giniewicz.it",
    user = "team22",
    password = "te@mzazz",
    database = "team22"
)

if(con):
    print("Połączenie udane")
else:
    print("Połączenie nieudane")



# Scieżka do plików csv.
csv_table_path: path.Path = path.Path().cwd()/"Tabele_csv"

def delete_table(table_name:str):
    # Połączenie z bazą danych (zmienna `con` już istnieje)
    cursor = con.cursor()


    # Zapytanie SQL usuwające tabelę
    drop_table_query = f"DROP TABLE IF EXISTS `{table_name}`;"

    # Wykonanie zapytania
    cursor.execute(drop_table_query)

    # Zatwierdzenie zmiany.
    con.commit()

    # Zamknięcie kursora
    cursor.close()



def create_table(df:pd.DataFrame, table_name:str,create_table_query:str) -> None:
    cursor = con.cursor()


    # Stwórz tabelę.
    cursor.execute(create_table_query)

    insert_query = f"INSERT INTO `{table_name}` ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"

    # Przekształcenie danych na listę krotek
    data_to_insert = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Wykonanie zapytań wstawiających dane
    print(f"Tworzenie {table_name}")
    cursor.executemany(insert_query, data_to_insert)

    # Zatwierdzenie transakcji
    con.commit()

    # Zamknięcie kursora
    cursor.close()


# Słownik zawierający zapytania tworzące każdą tabelę csv.
creative_queries:dict[str, str] = {
    "Atrakcje_db.csv": """
CREATE TABLE IF NOT EXISTS `Atrakcje` (
    `id_atrakcji` INT PRIMARY KEY,
    `id_miasta` INT,
    `atrakcja` VARCHAR(50)
);
""",

"Klienci_db.csv": """
CREATE TABLE IF NOT EXISTS `Klienci` (
    `id_klienta` INT PRIMARY KEY,
    `imie` VARCHAR(20),
    `nazwisko` VARCHAR(60),
    `data_urodzenia` DATE,
    `znizka` FLOAT,
    `adres_email` VARCHAR(60),
    `numer_telefonu` VARCHAR(10),
    `status_studenta` BOOL
);
""",

"Osoby_bliskie_db.csv" : """
CREATE TABLE IF NOT EXISTS `Osoby_bliskie` (
    `id_osoby_bliskiej` INT PRIMARY KEY,
    `imie` VARCHAR(20),
    `nazwisko` VARCHAR(60),
    `adres_email` VARCHAR(60),
    `numer_telefonu` VARCHAR(10)
);
""",

"Pracownicy_db.csv": """
CREATE TABLE IF NOT EXISTS `Pracownicy` (
    `id_pracownika` INT PRIMARY KEY,
    `imie` VARCHAR(20),
    `nazwisko` VARCHAR(60),
    `stanowisko` VARCHAR(15),
    `numer_telefonu` VARCHAR(10),
    `adres_email` VARCHAR(60)
);
""",

"Relacje_bliskości_db.csv":"""
CREATE TABLE IF NOT EXISTS `Relacje_bliskości` (
    `id_klienta` INT,
    `id_osoby_bliskiej` INT,
    PRIMARY KEY (`id_klienta`, `id_osoby_bliskiej`)
);
""",

"Transakcje_db.csv": """
CREATE TABLE IF NOT EXISTS `Transakcje` (
    `id_transakcji` INT PRIMARY KEY,
    `kwota` FLOAT,
    `data_transakcji` DATE,
    `id_klienta` INT,
    `id_wycieczki` INT
);
""",

"Wycieczki_db.csv": """
CREATE TABLE IF NOT EXISTS `Wycieczki` (
    `id_wycieczki` INT PRIMARY KEY,
    `data_rozpoczecia` DATE,
    `odbyla_sie` BOOL,
    `id_miasta` INT
);
""", 

"Wycieczki_pracownicy_db.csv": """
CREATE TABLE IF NOT EXISTS `Wycieczki_pracownicy` (
    `id_pracownika` INT,
    `id_wycieczki` INT,
    PRIMARY KEY (`id_pracownika`, `id_wycieczki`)
);
""",

"Wynagrodzenie_db.csv":"""
CREATE TABLE IF NOT EXISTS `Wynagrodzenie` (
    `stanowisko` VARCHAR(15) PRIMARY KEY,
    `wynagrodzenie` FLOAT
);
""",
"Miasta_db.csv":"""
CREATE TABLE IF NOT EXISTS `Miasta` (
    `id_miasta` INT PRIMARY KEY,
    `miasto` VARCHAR(50),
    `cena_wyjazdu` FLOAT,
    `matematyk` VARCHAR(75),
    `dlugosc_wycieczki` INT
);
"""
}


for csv_table_name in creative_queries.keys():
    # Znajdź nazwę tabeli, którą będzie nosić ta tabela SQL.
    sql_table_name: str = csv_table_name[:csv_table_name.find("_db")]

    creation_query: str = creative_queries[csv_table_name]

    delete_table(sql_table_name)

    csv_table: pd.DataFrame = pd.read_csv(csv_table_path/csv_table_name,
                                          sep = ";",
                                          encoding = "utf-8")
    
    create_table(csv_table, sql_table_name, creation_query)

