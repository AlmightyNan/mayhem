import mysql.connector as msc
from src.utils import CustomLogger as logger

# Initialize the logger
logger = logger()

# Configuration to establish MySQL connection
host = "localhost"
user = "root"
password = ""
accentColor = "black"
fontColor = "white"
projectName = "project mayhem"

# Initialize database connection
connection = msc.connect(
    host=host,
    user=user,
    password=password
)
