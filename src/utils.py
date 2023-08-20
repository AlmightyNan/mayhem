import datetime
import os

class CustomLogger:
    """
    Coloured logging with timestamp and custom types.
    Authors: AlmightyNan
    """

    os.system('')
    # Define ANSI escape codes for colored output
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94;1m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

    def __init__(self):
        pass

    def get_timestamp(self):
        """Get the current timestamp in HH:MM:SS AM/PM format."""
        now = datetime.datetime.now().strftime("%I:%M:%S %p")
        return f"[{now}]"

    def log(self, level, message):
        """Print a colored log message to stdout based on the levels."""
        log_levels = {
            "START": self.CYAN,
            "SUCCESS": self.GREEN,
            "INFO": self.CYAN,
            "ERROR": self.RED,
            "DEBUG": self.BLUE,
            "WARNING": self.YELLOW,
        }
        timestamp = self.get_timestamp()
        formatted_message = f"{timestamp} › {log_levels.get(level, '')}{level: <8}{self.RESET} {message}"
        print(formatted_message)

if __name__ == "__main__":
    # Create an instance of the CustomLogger class
    logger = CustomLogger()
