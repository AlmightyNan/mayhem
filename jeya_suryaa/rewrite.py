import pandas as pd
import curses
import re  # For regular expressions
from prettytable import PrettyTable
from math import *
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import numpy as np
import csv
import logging
import easygui


def logging_events():
    # Configure the logging module to write logs to a file
    logging.basicConfig(filename="app.log", level=logging.INFO)

    # Log an informational message
    logging.info("Application started")


def export_data_to_csv(df):
    file_path = easygui.filesavebox(default=".csv", filetypes=["*.csv"])

    if file_path:
        try:
            df.to_csv(file_path, index=False)
            logging.info(f"Data exported to {file_path}")
            print(f"Data exported to {file_path}")
        except Exception as e:
            logging.error(f"Error exporting data to CSV: {e}", exc_info=True)
            print(f"Error exporting data to CSV: {e}")


def load_data(file_path):
    try:
        # Define a custom function to handle the mixed data types
        def custom_converter(value):
            # Remove commas and quotation marks from numeric values
            value = re.sub(r'[,"]', "", str(value))
            try:
                # Try converting the cleaned value to a float
                return float(value)
            except ValueError:
                # If it's not a valid float, return it as a string
                return str(value)

        # Use the custom converter when reading the CSV
        df = pd.read_csv(
            file_path,
            converters={
                "Open": custom_converter,
                "High": custom_converter,
                "Low": custom_converter,
            },
        )
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def display_centered_text(stdscr, text):
    height, width = stdscr.getmaxyx()
    y = height // 2
    x = (width - len(text)) // 2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def plot_data(statistics):
    # Extract labels and values from the statistics dictionary
    labels = list(statistics.keys())
    values = list(statistics.values())

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, values, color="skyblue")
    plt.xlabel("Values")
    plt.title("Statistics Horizontal Bar Chart")
    plt.grid(axis="x", linestyle="--", alpha=0.6)

    # Annotate the bars with their values on the right side of the bars
    for label, value in zip(labels, values):
        if np.isfinite(value):
            plt.text(
                value,
                label,
                f"{value:.2f}",
                va="center",
                color="black",
                fontweight="bold",
                fontsize=10,
                ha="left" if value < 0 else "right",
            )

    # Set custom x-axis ticks
    max_x = 36000
    plt.xticks(np.arange(0, max_x + 1, 5000))  # Adjust the step as needed

    plt.tight_layout()
    plt.show()


def main(stdscr):
    logging_events()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    file_path = "/home/almightynan/Desktop/mayhem/mayhem/jeya_suryaa/stock analysis.csv"
    df = load_data(file_path)

    if df is None:
        return

    options = [
        "Analyze Open Column",
        "Analyze High Column",
        "Analyze Low Column",
        "Export Data as CSV",
        "Quit",
    ]
    current_option = 0  # Initialize the current option

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        try:
            for i, option in enumerate(options):
                x = (width - len(option)) // 2
                y = height // 2 - len(options) + i

                if i == current_option:
                    stdscr.addstr(y, x, f"> {option} <", curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, f"  {option}  ")

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and current_option > 0:
                current_option -= 1
            elif key == curses.KEY_DOWN and current_option < len(options) - 1:
                current_option += 1
            elif key == 10:  # Enter key
                if current_option == len(options) - 1:
                    break  # Quit the program
                elif current_option == len(options) - 2:  # "Export Data as CSV" option
                    export_data_to_csv(df)
                else:
                    column_name = options[current_option].split()[-2]
                    analyze_column_stats(stdscr, df, column_name)
        except Exception as e:
            logging.error(f"Error loading data: {e}", exc_info=True)


# Modify the analyze_column_stats function to center-align the response
def analyze_column_stats(stdscr, df, column_name):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Perform analysis on the specified column
    if column_name in df.columns:
        column = df[column_name]
        # Existing statistics
        mean = column.mean()
        std_dev = column.std()
        min_value = column.min()
        max_value = column.max()
        median = column.median()
        sum_value = column.sum()
        count = column.count()
        unique_count = len(column.unique())
        variance = column.var()
        skewness = column.skew()
        kurtosis = column.kurt()

        # Additional statistics
        quartiles = column.quantile([0.1, 0.25, 0.5, 0.75, 0.9])
        q10 = quartiles[0.1]
        q25 = quartiles[0.25]
        q50 = quartiles[0.5]
        q75 = quartiles[0.75]
        q90 = quartiles[0.9]
        iqr = q75 - q25
        mode = column.mode().values[0]
        range_value = max_value - min_value
        coef_variation = (std_dev / mean) * 100
        sem = std_dev / (count**0.5)
        mad = (column - median).abs().mean()
        cv = (mad / mean) * 100
        sum_of_squares = (column - mean).pow(2).sum()
        variance_of_sample = sum_of_squares / (count - 1)
        kurtosis_excess = kurtosis - 3
        log_mean = column.apply(lambda x: log(x)).mean()
        log_std_dev = column.apply(lambda x: log(x)).std()
        min_abs = column.abs().min()
        max_abs = column.abs().max()
        min_pos = column.where(lambda x: x > 0).min()
        max_pos = column.where(lambda x: x > 0).max()
        min_neg = column.where(lambda x: x < 0).min()
        max_neg = column.where(lambda x: x < 0).max()
        skew_abs = column.abs().skew()
        kurt_abs = column.abs().kurt()

        # Create a PrettyTable
        table = PrettyTable()
        table.field_names = ["Statistic", "Value"]
        # Add the additional statistics to the PrettyTable
        table.add_row(["Variance", f"{variance:.2f}"])
        table.add_row(["Skewness", f"{skewness:.2f}"])
        table.add_row(["Kurtosis", f"{kurtosis:.2f}"])
        table.add_row(["10th Percentile", f"{q10:.2f}"])
        table.add_row(["25th Percentile", f"{q25:.2f}"])
        table.add_row(["50th Percentile", f"{q50:.2f}"])
        table.add_row(["75th Percentile", f"{q75:.2f}"])
        table.add_row(["90th Percentile", f"{q90:.2f}"])
        table.add_row(["Interquartile Range", f"{iqr:.2f}"])
        table.add_row(["Mode", f"{mode:.2f}"])
        table.add_row(["Range", f"{range_value:.2f}"])
        table.add_row(["Coefficient of Variation", f"{coef_variation:.2f}%"])
        table.add_row(["Standard Error of the Mean", f"{sem:.2f}"])
        table.add_row(["Mean Absolute Deviation", f"{mad:.2f}"])
        table.add_row(["CV (MAD/mean)", f"{cv:.2f}%"])
        table.add_row(["Sum of Squares", f"{sum_of_squares:.2f}"])
        table.add_row(["Variance (Sample)", f"{variance_of_sample:.2f}"])
        table.add_row(["Kurtosis (Excess)", f"{kurtosis_excess:.2f}"])
        table.add_row(["Log Mean", f"{log_mean:.2f}"])
        table.add_row(["Log Std Dev", f"{log_std_dev:.2f}"])
        table.add_row(["Min (Absolute)", f"{min_abs:.2f}"])
        table.add_row(["Max (Absolute)", f"{max_abs:.2f}"])
        table.add_row(["Min (Positive)", f"{min_pos:.2f}"])
        table.add_row(["Max (Positive)", f"{max_pos:.2f}"])
        table.add_row(["Min (Negative)", f"{min_neg:.2f}"])
        table.add_row(["Max (Negative)", f"{max_neg:.2f}"])
        table.add_row(["Skewness (Absolute)", f"{skew_abs:.2f}"])
        table.add_row(["Kurtosis (Absolute)", f"{kurt_abs:.2f}"])

        # After calculating the statistics, create a dictionary
        statistics_dict = {
            # "Variance": variance,
            "Skewness": skewness,
            "Kurtosis": kurtosis,
            "10th Percentile": q10,
            "25th Percentile": q25,
            "50th Percentile": q50,
            "75th Percentile": q75,
            "90th Percentile": q90,
            "Interquartile Range": iqr,
            "Mode": mode,
            "Range": range_value,
            "Coefficient of Variation": coef_variation,
            "Standard Error of the Mean": sem,
            "Mean Absolute Deviation": mad,
            "CV (MAD/mean)": cv,
            "Kurtosis (Excess)": kurtosis_excess,
            "Log Mean": log_mean,
            "Log Std Dev": log_std_dev,
            "Min (Absolute)": min_abs,
            "Max (Absolute)": max_abs,
            "Min (Positive)": min_pos,
            "Max (Positive)": max_pos,
            "Min (Negative)": min_neg,
            "Max (Negative)": max_neg,
            "Skewness (Absolute)": skew_abs,
            "Kurtosis (Absolute)": kurt_abs,
        }

        # Call the plot_data function with the statistics dictionary
        # Get the table as a string
        table_text = table.get_string()

        # Calculate the starting y-coordinate for vertical centering
        y = (height - table.get_string().count("\n")) // 2

        # Calculate the starting x-coordinate for horizontal centering
        x = (width - max(len(line) for line in table_text.split("\n"))) // 2

        while True:
            stdscr.clear()
            for i, line in enumerate(table_text.split("\n")):
                stdscr.addstr(y + i, x, line)

            header_text = f"Analyzing {column_name} Column"
            footer_text = (
                f"Press 'q' and enter to exit this view and return back to menu."
            )
            stdscr.addstr(
                0, (width - len(header_text)) // 2, header_text, curses.A_BOLD
            )

            footer_text = (
                "Press 'q' and enter to exit this view and return back to menu."
            )
            stdscr.addstr(
                height - 2,
                (width - len(footer_text)) // 2,
                footer_text,
                curses.color_pair(1),
            )  # Red color

            stdscr.refresh()

            key = stdscr.getch()
            if key == ord("q"):
                break

        # Calculate the starting y-coordinate for the plot prompt at the footer
        plot_prompt_y = height - 2

        plot_prompt = "Do you want to plot this data? (yes/no): "
        stdscr.addstr(
            plot_prompt_y,
            (width - len(plot_prompt)) // 2,
            plot_prompt,
            curses.color_pair(1),
        )  # Red color
        stdscr.refresh()

        # Capture user input for plotting
        input_x = (width - len(plot_prompt)) // 2 + len(plot_prompt)
        input_y = plot_prompt_y
        user_input = ""
        # Clear the line where footer_text is displayed
        stdscr.addstr(height - 2, 0, " " * width)

        plot_prompt = "Do you want to plot this data? (yes/no): "
        stdscr.addstr(
            plot_prompt_y,
            (width - len(plot_prompt)) // 2,
            plot_prompt,
            curses.color_pair(1),
        )  # Red color
        stdscr.refresh()

        # Capture user input for plotting
        input_x = (width - len(plot_prompt)) // 2 + len(plot_prompt)
        input_y = plot_prompt_y
        user_input = ""
        while True:
            key = stdscr.getch()
            if key == 10:  # Enter key
                break
            elif key == 127:  # Backspace key
                user_input = user_input[:-1]
            elif key == ord("q"):  # If 'q' is typed, clear the line and ask again
                user_input = ""
                stdscr.addstr(
                    input_y, input_x, " " * (width - input_x)
                )  # Clear the line
            else:
                user_input += chr(key)

            stdscr.addstr(input_y, input_x, user_input)
            stdscr.refresh()

            if user_input.lower() == "yes":
                plot_data(statistics_dict)
                # After the graph is closed, clear the plot_prompt line and display it again
                stdscr.addstr(
                    input_y, input_x, " " * (width - input_x)
                )  # Clear the line
            elif user_input.lower() == "no":
                break

    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    logging_events()
    curses.wrapper(main)
