import mysql.connector as msc
from src.utils import CustomLogger as logger

logger = logger()

class Initialize:
    """Queries sent to the database on startup"""

    def db(db):
        logger.log(
            "SUCCESS", "Handshake success, sending queries to create database..."
        )
        # Create a database named 'library' if it doesn't exist
        db.execute("CREATE DATABASE IF NOT EXISTS library;")
        # Switch to the 'library' database for further operations
        db.execute("USE library;")

    def movies(db):
        logger.log("DEBUG", "Creating table 'movies'...")
        try:
            # Create the 'movies' table if it doesn't exist, with specific columns and data types
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS movies (
                    id INT(5) PRIMARY KEY,
                    title VARCHAR(100) UNIQUE NOT NULL,
                    overview TEXT,
                    original_language VARCHAR(10) DEFAULT 'Unknown'
                    vote_count int(5) DEFAULT 1,
                    vote_average int(5) DEFAULT 1 
                );
                """
            )
            logger.log(
                "SUCCESS", "Created table 'movies', switching to the next statement..."
            )
            # Commit the changes to the database after the successful table creation
            db.execute("COMMIT;")
        except msc.Error as err:
            # If the 'movies' table already exists, skip the table creation
            if err.errno == msc.errorcode.ER_TABLE_EXISTS_ERROR:
                logger.log("WARNING", "Existing table 'movies' found, skipping...")