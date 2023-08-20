import mysql.connector as msc
from src.utils import CustomLogger as logger
import pandas as pd
from unidecode import unidecode

# Initialize the logger
logger = logger()

class Insert:
    """Class to insert extracted values from a CSV file into the SQL table"""

    @staticmethod
    def from_csv(db, csv_file_path):
        # Log debug information: Reading data from the CSV file
        logger.log("DEBUG", f"Reading data from CSV file: {csv_file_path}")

        try:
            # Read the CSV file into a pandas DataFrame
            csv_data = pd.read_csv(csv_file_path)

            # Create the 'movies' table if it does not exist
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS movies (
                    id INT(5) PRIMARY KEY,
                    title VARCHAR(100) UNIQUE NOT NULL,
                    overview TEXT DEFAULT NULL,
                    original_language VARCHAR(10) DEFAULT 'Unknown',
                    vote_count INT(5) DEFAULT 0,
                    vote_average INT(5) DEFAULT 0
                );
                """
            )
            logger.log("SUCCESS", "Created table 'movies', switching to the next statement...")
            db.execute("COMMIT;")  # Commit the transaction after table creation

            logger.log("DEBUG", "Inserting data into table 'movies'...")

            # SQL query to insert data into the 'movies' table
            insert_query = "INSERT INTO movies (id, title, overview, original_language, vote_count, vote_average) VALUES (%s, %s, %s, %s, %s, %s)"

            # Set 'cursor' as 'db', assuming that 'db' is a MySQL cursor
            cursor = db

            # Loop through each row in the CSV data and insert it into the table
            for _, row in csv_data.iterrows():
                id = int(row["id"])

                # Preprocess the 'title', 'overview', and 'original_language' fields
                title = str(row["title"])[:100]
                title = "".join(["*" if c in "!@#$%^&*" else c for c in title])
                title = unidecode(title)

                overview = str(row["overview"])
                overview = "".join(["*" if c in "!@#$%^&*" else c for c in overview])
                overview = unidecode(overview)

                original_language = str(row["original_language"])[:10]
                original_language = "".join(
                    ["*" if c in "!@#$%^&*" else c for c in original_language]
                )
                original_language = unidecode(original_language)

                vote_count = int(row["vote_count"])
                vote_average = int(row["vote_average"])

                # Values to be inserted into the 'movies' table for the current row
                values = (
                    id,
                    title,
                    overview,
                    original_language,
                    vote_count,
                    vote_average,
                )

                try:
                    # Execute the insert query with the current row's values
                    cursor.execute(insert_query, values)
                    cursor.execute("COMMIT;")  # Commit the transaction after insertion
                except msc.Error as err:
                    # If the row is a duplicate entry, log a warning and skip
                    if err.errno == msc.errorcode.ER_DUP_ENTRY:
                        logger.log(
                            "WARNING",
                            f"Duplicate entry: {values}. Skipping to prevent duplicates...",
                        )
                    else:
                        logger.log(
                            "ERROR",
                            f"An error occurred while inserting row: {values}. Error: {err}",
                        )
                        db.execute("ROLLBACK;")  # Rollback the transaction
                        break  # Exit the loop on the first error

            logger.log("SUCCESS", "Inserted data from CSV into the 'movies' table.")
        except msc.Error as err:
            # Log an error if an error occurs during the process
            logger.log("ERROR", f"An error occurred: {err}")
            db.execute("ROLLBACK;")  # Rollback the transaction
