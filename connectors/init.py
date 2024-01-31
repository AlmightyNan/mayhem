from connectors.config import connection
from src.utils import CustomLogger as logger
import mysql.connector as msc 

logger = logger()

class Initialize:
    @staticmethod
    def db(connection):
        logger.log(
            "SUCCESS", "Handshake success, sending queries to create database..."
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS db;")
        cursor.execute("USE db;")
        cursor.close()

    @staticmethod
    def colleges(connection):
        logger.log("DEBUG", "Creating table 'colleges'...")
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS colleges (
                    College_Name MEDIUMTEXT,
                    Genders_Accepted MEDIUMTEXT,
                    Campus_Size MEDIUMTEXT,
                    Total_Student_Enrollments int(100),
                    Total_Faculty int(100),
                    Established_Year int(40),
                    Rating float(20, 10),
                    University MEDIUMTEXT,
                    Courses MEDIUMTEXT,
                    Facilities MEDIUMTEXT,
                    City MEDIUMTEXT,
                    State MEDIUMTEXT,
                    Country MEDIUMTEXT,
                    College_Type MEDIUMTEXT,
                    Average_Fees float(10, 10)
                );
                """
            )
            logger.log(
                "SUCCESS", "Created table 'colleges', switching to the next statement..."
            )
            cursor.execute("COMMIT;")
            cursor.close()
        except msc.Error as err:
            if err.errno == msc.errorcode.ER_TABLE_EXISTS_ERROR:
                logger.log("WARNING", "Existing table 'colleges' found, skipping...")
