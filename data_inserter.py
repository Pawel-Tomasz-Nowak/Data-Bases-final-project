import mysql.connector
import pandas as pd
import pathlib as path

# Establish a connection to the MySQL database.
# Replace with your actual database credentials.
con = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)

if(con):
    print("Connection successful")
else:
    print("Connection failed")



# Path to the CSV files.
csv_table_path: path.Path = path.Path().cwd()/"CSV_Tables"

def delete_table(table_name:str):
    """
    Deletes a table from the database if it exists.

    Args:
        table_name (str): The name of the table to delete.
    """
    # The database connection (`con`) already exists.
    cursor = con.cursor()


    # SQL query to drop the table.
    drop_table_query = f"DROP TABLE IF EXISTS `{table_name}`;"

    # Execute the query.
    cursor.execute(drop_table_query)

    # Commit the change.
    con.commit()

    # Close the cursor.
    cursor.close()



def create_table(df:pd.DataFrame, table_name:str,create_table_query:str) -> None:
    """
    Creates a table in the database and inserts data from a pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to insert.
        table_name (str): The name of the table to create.
        create_table_query (str): The SQL query to create the table.
    """
    cursor = con.cursor()


    # Create the table.
    cursor.execute(create_table_query)

    # Prepare the insert query.
    insert_query = f"INSERT INTO `{table_name}` ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"

    # Convert data to a list of tuples.
    data_to_insert = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Execute the insert queries.
    print(f"Creating {table_name}")
    cursor.executemany(insert_query, data_to_insert)

    # Commit the transaction.
    con.commit()

    # Close the cursor.
    cursor.close()


# Dictionary containing the CREATE TABLE queries for each CSV file.
creative_queries:dict[str, str] = {
    "Attractions_db.csv": """
CREATE TABLE IF NOT EXISTS `Attractions` (
    `attraction_id` INT PRIMARY KEY,
    `city_id` INT,
    `attraction` VARCHAR(50)
);
""",

"Clients_db.csv": """
CREATE TABLE IF NOT EXISTS `Clients` (
    `client_id` INT PRIMARY KEY,
    `first_name` VARCHAR(20),
    `last_name` VARCHAR(60),
    `birth_date` DATE,
    `discount` FLOAT,
    `email_address` VARCHAR(60),
    `phone_number` VARCHAR(10),
    `student_status` BOOL
);
""",

"Relatives_db.csv" : """
CREATE TABLE IF NOT EXISTS `Relatives` (
    `relative_id` INT PRIMARY KEY,
    `first_name` VARCHAR(20),
    `last_name` VARCHAR(60),
    `email_address` VARCHAR(60),
    `phone_number` VARCHAR(10)
);
""",

"Employees_db.csv": """
CREATE TABLE IF NOT EXISTS `Employees` (
    `employee_id` INT PRIMARY KEY,
    `first_name` VARCHAR(20),
    `last_name` VARCHAR(60),
    `position` VARCHAR(15),
    `phone_number` VARCHAR(10),
    `email_address` VARCHAR(60)
);
""",

"Relationships_db.csv":"""
CREATE TABLE IF NOT EXISTS `Relationships` (
    `client_id` INT,
    `relative_id` INT,
    PRIMARY KEY (`client_id`, `relative_id`)
);
""",

"Transactions_db.csv": """
CREATE TABLE IF NOT EXISTS `Transactions` (
    `transaction_id` INT PRIMARY KEY,
    `amount` FLOAT,
    `transaction_date` DATE,
    `client_id` INT,
    `trip_id` INT
);
""",

"Trips_db.csv": """
CREATE TABLE IF NOT EXISTS `Trips` (
    `trip_id` INT PRIMARY KEY,
    `start_date` DATE,
    `took_place` BOOL,
    `city_id` INT
);
""", 

"Trips_employees_db.csv": """
CREATE TABLE IF NOT EXISTS `Trips_employees` (
    `employee_id` INT,
    `trip_id` INT,
    PRIMARY KEY (`employee_id`, `trip_id`)
);
""",

"Salary_db.csv":"""
CREATE TABLE IF NOT EXISTS `Salary` (
    `position` VARCHAR(15) PRIMARY KEY,
    `salary` FLOAT
);
""",
"Cities_db.csv":"""
CREATE TABLE IF NOT EXISTS `Cities` (
    `city_id` INT PRIMARY KEY,
    `city` VARCHAR(50),
    `trip_price` FLOAT,
    `mathematician` VARCHAR(75),
    `trip_duration` INT
);
"""
}


for csv_table_name in creative_queries.keys():
    # Find the name of the SQL table.
    sql_table_name: str = csv_table_name[:csv_table_name.find("_db")]

    creation_query: str = creative_queries[csv_table_name]

    delete_table(sql_table_name)

    csv_table: pd.DataFrame = pd.read_csv(csv_table_path/csv_table_name,
                                          sep = ";",
                                          encoding = "utf-8")
    
    create_table(csv_table, sql_table_name, creation_query)


