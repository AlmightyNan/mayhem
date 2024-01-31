import mysql.connector as msc
from src.utils import CustomLogger as logger
import pandas as pd

logger = logger()

class Insert:
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
    def from_csv(db, csv_file_path):
        logger.log("DEBUG", f"Reading data from CSV file: {csv_file_path}")
        try:
            cursor = db.cursor()
            csv_data = pd.read_csv(csv_file_path)

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
            logger.log("SUCCESS", "Created table 'colleges', switching to the next statement...")
            cursor.execute("COMMIT;")

            logger.log("DEBUG", "Inserting data into table 'colleges'...")

            insert_query = "INSERT INTO colleges (College_Name, Genders_Accepted, Campus_Size, Total_Student_Enrollments, Total_Faculty, Established_Year, Rating, University, Courses, Facilities, City, State, Country, College_Type, Average_Fees) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = db.cursor()

            for _, row in csv_data.iterrows():
                college_name = row['College Name']
                gender_accepted = row['Genders Accepted']
                campus_size = row['Campus Size']
                total_student_enrollments = row['Total Student Enrollments']
                total_faculty = row['Total Faculty']
                established_year = row['Established Year']
                rating = row['Rating']
                university = row['University']
                courses = row['Courses']
                facilities = row['Facilities']
                city = row['City']
                state = row['State']
                country = row['Country']
                college_type = row['College Type']
                average_fees = row['Average Fees']
                
                values = (
                    college_name,
                    gender_accepted,
                    campus_size,
                    total_student_enrollments,
                    total_faculty,
                    established_year,
                    rating,
                    university,
                    courses,
                    facilities,
                    city,
                    state,
                    country,
                    college_type,
                    average_fees
                )

                values = tuple(None if pd.isna(val) else val for val in values)

                try:
                    cursor.execute(insert_query, values)
                    cursor.execute("COMMIT;")
                except msc.Error as err:
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
                        cursor.execute("ROLLBACK;")
                        break

            logger.log("SUCCESS", "Inserted data from CSV into the 'colleges' table.")
        except msc.Error as err:
            logger.log("ERROR", f"An error occurred: {err}")
            cursor.execute("ROLLBACK;")
