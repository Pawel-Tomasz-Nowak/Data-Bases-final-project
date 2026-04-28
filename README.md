# 🏛️ Database for "Wombat Grylls Ltd." Travel Agency 🏛️

## 🚀 Introduction

Welcome to the repository for the "Wombat Grylls Ltd." travel agency database project! This project is designed to manage a comprehensive database for a company specializing in trips to cities of historical significance in mathematics. It efficiently handles data for clients, employees, trips, transactions, and tourist attractions.

This repository is the home for our final project from the databases course.

## 🎯 Project Goal

The primary goal is to provide the company with a robust tool for:
-   Efficient management of operational data.
-   In-depth analysis of sales data and trip popularity.
-   Streamlined logistics and human resource planning.
-   Monitoring financial results and profitability.
-   Supporting data-driven business decisions.

## 🗄️ Database Structure

The database follows a relational model and includes tables for cities, attractions, clients, employees, trips, and more.

Below is the database schema:

![Database Schema](schemat_bazy.vuerd.png)

## 📁 Project File Structure

-   `data_generator.ipynb`: Jupyter Notebook to generate synthetic data.
-   `data_inserter.py`: Python script to create the database structure and import data.
-   `report.Rmd`: R Markdown file for data analysis and report generation.
-   `report.html`: The generated HTML report with business analyses.
-   `requirements.txt`: A list of all the necessary Python dependencies.
-   `setup_venv.bat`: Automated script for setting up the virtual environment on Windows.
-   `setup_venv.sh`: Automated script for setting up the virtual environment on macOS/Linux.
-   `schemat_bazy.vuerd`: Vuerd file containing the visual database model.
-   `CSV_Tables/`: Directory for the generated `.csv` data files.
-   `documentation/`: Directory with additional project documentation.
-   `Names/`: Directory with data for the data generator.

## 🏁 Getting Started

### Prerequisites

-   Python 3.x
-   A running MySQL database server.
-   R environment (like RStudio) with `RMariaDB`, `dplyr`, `ggplot2`, `plotly`, `kableExtra` packages installed.

### Installation & Setup

1.  **Set up the Python Environment**:
    -   **Windows**: Run the `setup_venv.bat` script by double-clicking it.
    -   **macOS/Linux**: Open a terminal and run `bash setup_venv.sh`.
    This will create a virtual environment and install all required Python packages.

2.  **Activate the Virtual Environment**:
    -   **Windows**: `.venv\Scripts\activate`
    -   **macOS/Linux**: `source .venv/bin/activate`

3.  **Data Generation**:
    -   Run the `data_generator.ipynb` notebook in a Jupyter environment (available after setup).
    -   Execute all cells to generate the `.csv` files in the `CSV_Tables/` directory.

4.  **Database Configuration and Creation**:
    -   In the `data_inserter.py` file, configure the connection to your database in the `mysql.connector.connect()` function.
    -   Run the `data_inserter.py` script (`python data_inserter.py`) to create the tables and import the data.

5.  **Report Generation**:
    -   In the `report.Rmd` file, configure the database connection in the `db_connect` section.
    -   Use your R environment to "render" the `report.Rmd` file to HTML.

## 🛠️ Technologies

-   **Database**: MySQL
-   **Data Generation**: Python, Pandas, NumPy, Jupyter
-   **Database Automation**: Python, `mysql-connector-python`
-   **Analysis and Reporting**: R, R Markdown
-   **Database Modeling**: Vuerd

