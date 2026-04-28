# Database for "Wombat Grylls Ltd." Travel Agency

## Introduction

This project involves the creation and management of a comprehensive database for the "Wombat Grylls Ltd." company, which specializes in organizing trips to cities of historical significance in mathematics. The database is designed to efficiently collect and process information about clients, employees, trips, transactions, and tourist attractions.

## Project Goal

The main goal of the project is to provide the company with a tool for:
- Efficient management of operational data.
- Analysis of sales data and the popularity of individual trips.
- Planning logistics and human resources.
- Monitoring financial results and profitability.
- Supporting business decisions based on data.

## Database Structure

The database is designed in a relational model and consists of the following tables:

-   `Miasta` (Cities): Stores information about the cities to which trips are organized, along with the price, duration of the trip, and the associated mathematician.
-   `Atrakcje` (Attractions): Contains a list of tourist attractions in each city.
-   `Klienci` (Clients): Gathers data about the company's clients, including personal data, information about discounts, and student status.
-   `Osoby_bliskie` (Relatives): Stores contact details for clients' close relatives.
-   `Relacje_bliskości` (Relationships): A table linking clients with their close relatives.
-   `Pracownicy` (Employees): Contains data about the company's employees, such as guides and drivers.
-   `Wynagrodzenie` (Salaries): Defines the salary rates for different positions.
-   `Wycieczki` (Trips): Stores information about planned and completed trips.
-   `Transakcje` (Transactions): Records all financial transactions related to the purchase of trips by clients.
-   `Wycieczki_pracownicy` (Trips_Employees): A table linking employees with the trips they participate in.

Below is the database schema:

![Database Schema](schemat_bazy.vuerd.png)

## Project File Structure

-   `generator_danych.ipynb`: A Jupyter Notebook for generating synthetic data for the entire database. It allows for flexible creation of test data with specified parameters.
-   `Wstawiator_danych.py`: A Python script that creates the database structure (tables) and imports data from the generated `.csv` files.
-   `raport.Rmd`: An R Markdown file that connects to the database, performs analyses, and generates a report in HTML format (`raport.html`).
-   `raport.html`: The generated report with business analyses.
-   `schemat_bazy.vuerd`: A Vuerd database schema editor project file containing the visual model of the database.
-   `Tabele_csv/`: A directory containing the generated data in `.csv` format, ready for import.
-   `dokumentacja/`: A directory with additional project documentation.
-   `Imiona i nazwiska/`: A directory with data needed for the generator (first names, last names).

## How to Run the Project

1.  **Data Generation**:
    -   Run the `generator_danych.ipynb` notebook in a Jupyter environment.
    -   Execute all cells to generate the `.csv` files in the `Tabele_csv/` directory.

2.  **Database Configuration and Creation**:
    -   Make sure you have a running MySQL database server.
    -   In the `Wstawiator_danych.py` file, configure the connection to your database in the `mysql.connector.connect()` function.
    -   Run the `Wstawiator_danych.py` script (`python Wstawiator_danych.py`) to create the tables and import the data.

3.  **Report Generation**:
    -   In the `raport.Rmd` file, configure the database connection in the `db_connect` section.
    -   Use an R environment (e.g., RStudio) with the required packages installed (`RMariaDB`, `dplyr`, `ggplot2`, `plotly`, `kableExtra`) to "render" the `raport.Rmd` file to HTML.

## Technologies

-   **Database**: MySQL
-   **Data Generation**: Python, Pandas, NumPy
-   **Database Automation**: Python, `mysql-connector-python`
-   **Analysis and Reporting**: R, R Markdown
-   **Database Modeling**: Vuerd


This reposistory is the home for our final project from data bases course.
