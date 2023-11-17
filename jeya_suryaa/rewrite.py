import pandas as pd
import re
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, filedialog
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import sys
import time

# ANSI color escape codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
INDEX_COLOR = "\033[94m"  # Blue color for index numbers

def train_linear_regression_model(df, target_column, feature_columns):
    # Remove commas from numeric columns only
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].replace({',': ''}, regex=True)

    # Convert numeric columns to float
    df[numeric_columns] = df[numeric_columns].astype(float)

    # Drop rows with missing values in target or feature columns
    df = df.dropna(subset=[target_column] + feature_columns)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        df[feature_columns],
        df[target_column],
        test_size=0.2,
        random_state=42
    )

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')

    return model


# # Assuming you want to predict 'High' based on other columns
# target_column = 'High'
# feature_columns = ['Open', 'Low', 'Close', 'Adj Close', 'Volume', 'TURNOVER', 'Point Change', '% Change']
# prediction_model = train_linear_regression_model(df, target_column, feature_columns)

# # Now you can use the trained model to predict future values
# future_features = np.array([[...]])  # Replace ... with the values for your future prediction

def predict_future_values(model, feature_columns, future_features):
    future_prediction = model.predict(future_features)
    return future_prediction[0]

def export_data_to_csv(df):
    root = Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        try:
            df.to_csv(file_path, index=False)
            print(GREEN + f"Data exported to {file_path}" + RESET)
        except Exception as e:
            print(RED + f"Error exporting data to CSV: {e}" + RESET)


def load_data(file_path):
    try:

        def custom_converter(value):
            value = re.sub(r'[,"]', "", str(value))
            try:
                return float(value)
            except ValueError:
                return str(value)

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
        print(RED + f"Error loading data: {e}" + RESET)
        return None


def plot_data(statistics):
    labels = list(statistics.keys())
    values = list(statistics.values())

    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, values, color="skyblue")
    plt.xlabel("Values")
    plt.title("Statistics Horizontal Bar Chart")
    plt.grid(axis="x", linestyle="--", alpha=0.6)

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

    max_x = 36000
    plt.xticks(np.arange(0, max_x + 1, 5000))

    plt.tight_layout()
    plt.show()


def analyze_column_stats(df, column_name):
    user_input = input("Do you want to plot this data? (yes/no): ").lower()
    if user_input == "yes":
        # Plot line graph for Open, High, Low, Close, Adj Close, Volume
        if column_name in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
            plot_line_graph(
                df,
                ["Open", "High", "Low", "Close", "Adj Close", "Volume"],
                f"{column_name} Line Graph",
            )

        # Plot bar graph for LTP, CHNG, %CHNG, TURNOVER, 52 w-h
        elif column_name in ["LTP", "CHNG", "%CHNG", "TURNOVER", "52 w-h"]:
            plot_bar_graph(
                df,
                ["LTP", "CHNG", "%CHNG", "TURNOVER", "52 w-h"],
                f"{column_name} Bar Graph",
            )

    if column_name in df.columns:
        column = df[column_name]
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

        quartiles = column.quantile([0.1, 0.25, 0.5, 0.75, 0.9])
        q10, q25, q50, q75, q90 = (
            quartiles[0.1],
            quartiles[0.25],
            quartiles[0.5],
            quartiles[0.75],
            quartiles[0.9],
        )
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
        log_mean = column.apply(lambda x: np.log(x)).mean()
        log_std_dev = column.apply(lambda x: np.log(x)).std()
        min_abs = column.abs().min()
        max_abs = column.abs().max()
        min_pos = column.where(lambda x: x > 0).min()
        max_pos = column.where(lambda x: x > 0).max()
        min_neg = column.where(lambda x: x < 0).min()
        max_neg = column.where(lambda x: x < 0).max()
        skew_abs = column.abs().skew()
        kurt_abs = column.abs().kurt()

        statistics_dict = {
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

        table = PrettyTable()
        table.field_names = [BOLD + "Statistic" + RESET, BOLD + "Value" + RESET]
        for stat, value in statistics_dict.items():
            table.add_row([stat, f"{value:.2f}"])

        print(CYAN + f"Analyzing {column_name} Column\n" + RESET)
        print(table)

        user_input = input("Do you want to plot this data? (yes/no): ").lower()
        if user_input == "yes":
            plot_data(statistics_dict)


def plot_line_graph(df, columns, title):
    num_plots = len(columns)
    num_rows = (num_plots + 1) // 2  # Ensure at least two rows

    fig, axs = plt.subplots(num_rows, 2, figsize=(15, 4 * num_rows))

    for i, column in enumerate(columns):
        row_idx, col_idx = divmod(i, 2)
        axs[row_idx, col_idx].plot(df["Date"], df[column], label=column)
        axs[row_idx, col_idx].set_title(column)
        axs[row_idx, col_idx].set_xlabel("Date")
        axs[row_idx, col_idx].set_ylabel("Value")
        axs[row_idx, col_idx].legend()
        axs[row_idx, col_idx].grid(True)

        # Set xticks to only 3 values: start, middle, and end
        xticks = [
            df["Date"].iloc[0],
            df["Date"].iloc[len(df) // 2],
            df["Date"].iloc[-1],
        ]
        axs[row_idx, col_idx].set_xticks(xticks)
        axs[row_idx, col_idx].set_xticklabels([str(date) for date in xticks])

    # Remove any empty subplots
    for i in range(num_plots, num_rows * 2):
        fig.delaxes(axs.flatten()[i])

    plt.suptitle(title)
    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust layout to prevent title overlap
    plt.show()


def plot_bar_graph(df, columns, title):
    num_plots = len(columns)
    num_rows = (num_plots + 1) // 2  # Ensure at least two rows

    fig, axs = plt.subplots(num_rows, 2, figsize=(15, 4 * num_rows))

    for i, column in enumerate(columns):
        row_idx, col_idx = divmod(i, 2)
        axs[row_idx, col_idx].bar(df["Date"], df[column], label=column, color=f"C{i}")
        axs[row_idx, col_idx].set_title(column)
        axs[row_idx, col_idx].set_xlabel("Date")
        axs[row_idx, col_idx].set_ylabel("Value")
        axs[row_idx, col_idx].legend()
        axs[row_idx, col_idx].grid(True)

        # Set xticks to only 3 values: start, middle, and end
        xticks = [
            df["Date"].iloc[0],
            df["Date"].iloc[len(df) // 2],
            df["Date"].iloc[-1],
        ]
        axs[row_idx, col_idx].set_xticks(xticks)
        axs[row_idx, col_idx].set_xticklabels([str(date) for date in xticks])

    # Remove any empty subplots
    for i in range(num_plots, num_rows * 2):
        fig.delaxes(axs.flatten()[i])

    plt.suptitle(title)
    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust layout to prevent title overlap
    plt.show()


company_info = {
    'Reliance Industries': {
        'Industry': 'Conglomerate',
        'Website': 'https://www.ril.com/',
        'Description': 'Reliance Industries Limited is an Indian multinational conglomerate company.',
        'Founders': 'Dhirubhai Ambani',
        'Headquarters': 'Mumbai, Maharashtra, India',
        'Founded': '8 May 1973',
        'Stock Information': {
            'Index': 'NSE',
            'Date': 'May 09, 2022',
            'Open': 2337.69,
            'High': 2357.8,
            'Low': 2276.01,
            'Close': 2518.30,
            'Adj Close': 2510.74,
            'Volume': 8345649,
            'LTP': 715,
            'CHNG': -47.45,
            '%CHNG': -6.22,
            'TURNOVER': 532.63,
            '52 w-h': 901,
            'Point Change': 79.22,
            '% Change': -4.65
        }
    },
    'Tata Steel': {
        'Industry': 'Steel',
        'Website': 'https://www.tatasteel.com/',
        'Description': 'Tata Steel Limited is an Indian multinational steel-making company.',
        'Founders': 'Jamsetji Tata',
        'Headquarters': 'Mumbai, Maharashtra, India',
        'Founded': '25 August 1907',
        'Stock Information': {
            'Index': 'NSE',
            'Date': 'Jul 15, 2022',
            'Open': 90.5,
            'High': 91.03,
            'Low': 87.75,
            'Close': 88.38,
            'Adj Close': 85.59,
            'Volume': 81253510,
            'LTP': 3138.00,
            'CHNG': -6.25,
            '%CHNG': -0.2,
            'TURNOVER': 322.53,
            '52 w-h': 3505.00,
            'Point Change': 45.66,
            '% Change': 5.66
        }
    },
    'Tata Motors': {
        'Industry': 'Automotive',
        'Website': 'https://www.tatamotors.com/',
        'Description': 'Tata Motors Limited is an Indian multinational automotive manufacturing company.',
        'Founders': 'J.R.D. Tata',
        'Headquarters': 'Mumbai, Maharashtra, India',
        'Founded': '1945',
        'Stock Information': {
            'Index': 'NSE',
            'Date': 'Sep 08, 2022',
            'Open': 452.45,
            'High': 452.55,
            'Low': 440,
            'Close': 442.2,
            'Adj Close': 440.83,
            'Volume': 19336014,
            'LTP': 661,
            'CHNG': -18.9,
            '%CHNG': -2.78,
            'TURNOVER': 684,
            '52 w-h': 866.9,
            'Point Change': 10.19,
            '% Change': -21.49
        }
    },
    'HFCL': {
        'Industry': 'Telecommunications',
        'Website': 'https://www.hfcl.com/',
        'Description': 'Himachal Futuristic Communications Limited is an Indian telecommunications equipment manufacturer.',
        'Founders': 'Mahendra Nahata',
        'Headquarters': 'New Delhi, India',
        'Founded': '1987',
        'Stock Information': {
            'Index': 'NSE',
            'Date': 'Nov 02, 2022',
            'Open': 83.15,
            'High': 84.85,
            'Low': 82.05,
            'Close': 82.6,
            'Adj Close': 82.6,
            'Volume': 963087,
            'LTP': 3335.00,
            'CHNG': -56.7,
            '%CHNG': -1.67,
            'TURNOVER': 114.59,
            '52 w-h': 4361.40,
            'Point Change': 9.3,
            '% Change': -12.05
        }
    },
    'ITC': {
        'Industry': 'Conglomerate',
        'Website': 'https://www.itcportal.com/',
        'Description': 'ITC Limited is an Indian multinational conglomerate company.',
        'Founders': 'S. K. Puri',
        'Headquarters': 'Kolkata, West Bengal, India',
        'Founded': '24 August 1910',
        'Stock Information': {
            'Index': 'NSE',
            'Date': 'Mar 04, 2022',
            'Open': 217.7,
            'High': 227.4,
            'Low': 217,
            'Close': 225.5,
            'Adj Close': 215.58,
            'Volume': 66835736,
            'LTP': 16684.00,
            'CHNG': -684.85,
            '%CHNG': -3.94,
            'TURNOVER': 576.79,
            '52 w-h': 19325.00,
            'Point Change': 91.38,
            '% Change': -9.1
        }
    },
    'Adani Power': {
        'Industry': 'Electricity Generation',
        'Website': 'https://www.adanipower.com/',
        'Description': 'Adani Power Limited is the power business subsidiary of Indian conglomerate Adani Group.',
        'Founders': 'Gautam Adani',
        'Headquarters': 'Ahmedabad, Gujarat, India',
        'Founded': '1996',
        'Stock Information': {
            'Index': 'NSE',
            'Date': 'Jan 07, 2022',
            'Open': 101.4,
            'High': 102.45,
            'Low': 99.5,
            'Close': 100.2,
            'Adj Close': 100.2,
            'Volume': 4759250,
            'LTP': 6780.00,
            'CHNG': -345.8,
            '%CHNG': -4.85,
            'TURNOVER': 1161.63,
            '52 w-h': 8050.00,
            'Point Change': 44.57,
            '% Change': -13.69
        }
    },
    'NIFTY': {
    'Industry': 'Stock Market Index',
    'Website': 'https://www.nseindia.com/',
    'Description': 'NIFTY 50 is the flagship index on the National Stock Exchange of India Ltd. (NSE).',
    'Founders': 'National Stock Exchange of India Ltd. (NSE)',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': 'November 1992',
    'Stock Information': {
        'Index': 'Nifty 50',
        'Date': 'Nov 10, 2022',
        'Open': 18044.35,
        'High': 18103.10,
        'Low': 17969.40,
        'Close': 18028.20,
        'Adj Close': 18028.20,
        'Volume': 256500,
        'LTP': 735.85,
        'CHNG': -29.3,
        '%CHNG': -3.83,
        'TURNOVER': 830.06,
        '52 w-h': 781.8,
        'Point Change': 58.55,
        '% Change': 5.7
    }
},
'Apollo Micro Systems Ltd': {
    'Industry': 'Technology',
    'Website': 'https://www.apollomicrosystems.com/',
    'Description': 'Apollo Micro Systems Ltd is a technology company providing solutions in the defense and aerospace sectors.',
    'Founders': 'Karunakar Reddy Baddam',
    'Headquarters': 'Hyderabad, Telangana, India',
    'Founded': '1997',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Dec 12, 2022',
        'Open': 25.8,
        'High': 26.82,
        'Low': 25.3,
        'Close': 26.67,
        'Adj Close': 26.67,
        'Volume': 719790,
        'LTP': 377.4,
        'CHNG': -22.7,
        '%CHNG': -5.67,
        'TURNOVER': 383.54,
        '52 w-h': 503,
        'Point Change': -1.22,
        '% Change': -12.45
    }
},
'Reliance BP Mobility Ltd': {
    'Industry': 'Oil and Gas',
    'Website': 'https://www.bp.com/',
    'Description': 'Reliance BP Mobility Ltd is a joint venture between Reliance Industries and BP focused on the mobility and energy sector.',
    'Founders': 'Reliance Industries Limited, BP',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': 'March 01, 2022',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Mar 01, 2022',
        'Open': 28.78,
        'High': 29.33,
        'Low': 28.18,
        'Close': 28.49,
        'Adj Close': 26.68,
        'Volume': 24860000,
        'LTP': 3566.60,
        'CHNG': -6.8,
        '%CHNG': -0.19,
        'TURNOVER': 133.23,
        '52 w-h': 4153.00,
        'Point Change': 0.3,
        '% Change': -3.42
    }
},

'DJI': {
    'Industry': 'Stock Market Index',
    'Website': 'https://www.dowjones.com/',
    'Description': 'Dow Jones Industrial Average (DJI) is a stock market index that measures the stock performance of 30 large companies listed on stock exchanges in the United States.',
    'Founders': 'Charles Dow, Edward Jones, and Charles Bergstresser',
    'Headquarters': 'New York City, New York, USA',
    'Founded': 'May 26, 1896',
    'Stock Information': {
        'Index': 'DJI',
        'Date': 'Apr 05, 2022',
        'Open': 34876.33,
        'High': 35112.21,
        'Low': 34566.04,
        'Close': 34641.18,
        'Adj Close': 34641.18,
        'Volume': 30401000,
        'LTP': 965,
        'CHNG': 65.05,
        '%CHNG': 7.23,
        'TURNOVER': 1380.90,
        '52 w-h': 1005.00,
        'Point Change': 31.89,
        '% Change': 6.34
    }
},
'Google': {
    'Industry': 'Technology',
    'Website': 'https://www.google.com/',
    'Description': 'Google LLC is an American multinational technology company that specializes in Internet-related services and products.',
    'Founders': 'Larry Page and Sergey Brin',
    'Headquarters': 'Mountain View, California, USA',
    'Founded': 'September 4, 1998',
    'Stock Information': {
        'Index': 'NasdaqGS',
        'Date': 'Feb 15, 2022',
        'Open': 137.47,
        'High': 137.9,
        'Low': 135.54,
        'Close': 136.43,
        'Adj Close': 136.43,
        'Volume': 26578000,
        'LTP': 155.9,
        'CHNG': -2.65,
        '%CHNG': -1.67,
        'TURNOVER': 185.5,
        '52 w-h': 203.8,
        'Point Change': 25.78,
        '% Change': -10.94
    }
},
'Microsoft': {
    'Industry': 'Technology',
    'Website': 'https://www.microsoft.com/',
    'Description': 'Microsoft Corporation is an American multinational technology company that produces, licenses, and sells computer software, consumer electronics, and personal computers.',
    'Founders': 'Bill Gates and Paul Allen',
    'Headquarters': 'Redmond, Washington, USA',
    'Founded': 'April 4, 1975',
    'Stock Information': {
        'Index': 'NasdaqGS',
        'Date': 'Oct 05, 2022',
        'Open': 245.99,
        'High': 250.58,
        'Low': 244.1,
        'Close': 249.2,
        'Adj Close': 246.82,
        'Volume': 20347100,
        'LTP': 4940.00,
        'CHNG': 140.2,
        '%CHNG': 2.92,
        'TURNOVER': 775.37,
        '52 w-h': 5425.10,
        'Point Change': 42.39,
        '% Change': -1.57
    }
},
'Apple': {
    'Industry': 'Technology',
    'Website': 'https://www.apple.com/',
    'Description': 'Apple Inc. is an American multinational technology company that designs, manufactures, and markets consumer electronics, computer software, and online services.',
    'Founders': 'Steve Jobs, Steve Wozniak, and Ronald Wayne',
    'Headquarters': 'Cupertino, California, USA',
    'Founded': 'April 1, 1976',
    'Stock Information': {
        'Index': 'NasdaqGS',
        'Date': 'Jun 08, 2022',
        'Open': 148.58,
        'High': 149.87,
        'Low': 147.46,
        'Close': 147.96,
        'Adj Close': 146.88,
        'Volume': 53950200,
        'LTP': 4750.00,
        'CHNG': 158.4,
        '%CHNG': 3.45,
        'TURNOVER': 508.97,
        '52 w-h': 5614.60,
        'Point Change': -1.17,
        '% Change': 1.8
    }
},
'Tesla': {
    'Industry': 'Automotive and Energy',
    'Website': 'https://www.tesla.com/',
    'Description': 'Tesla, Inc. is an American electric vehicle and clean energy company.',
    'Founders': 'Elon Musk, Martin Eberhard, Marc Tarpenning, JB Straubel, and Ian Wright',
    'Headquarters': 'Palo Alto, California, USA',
    'Founded': 'July 1, 2003',
    'Stock Information': {
        'Index': 'NasdaqGS',
        'Date': 'Apr 11, 2022',
        'Open': 326.8,
        'High': 336.16,
        'Low': 324.88,
        'Close': 325.31,
        'Adj Close': 325.31,
        'Volume': 59357100,
        'LTP': 2440.75,
        'CHNG': -79.65,
        '%CHNG': -3.16,
        'TURNOVER': 136.56,
        '52 w-h': 3037.00,
        'Point Change': -5.95,
        '% Change': -5.77
    }
},
'SpaceX': {
    'Industry': 'Aerospace and Space Transportation',
    'Website': 'https://www.spacex.com/',
    'Description': 'Space Exploration Technologies Corp., known as SpaceX, is an American aerospace manufacturer and space transport services company.',
    'Founders': 'Elon Musk',
    'Headquarters': 'Hawthorne, California, USA',
    'Founded': 'March 14, 2002',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Sep 20, 2022',
        'Open': 699.9,
        'High': 715,
        'Low': 698.4,
        'Close': 706.15,
        'Adj Close': 700.14,
        'Volume': 2330872,
        'LTP': 1685.80,
        'CHNG': -80.95,
        '%CHNG': -4.58,
        'TURNOVER': 127.84,
        '52 w-h': 1893.00,
        'Point Change': 99.95,
        '% Change': -3.08
    }
},
'Bayerische Motoren Werke AG': {
    'Industry': 'Automotive',
    'Website': 'https://www.bmwgroup.com/',
    'Description': 'Bayerische Motoren Werke AG, commonly referred to as BMW, is a German multinational corporation that produces luxury vehicles and motorcycles.',
    'Founders': 'Franz Josef Popp, Karl Rapp, and Camillo Castiglioni',
    'Headquarters': 'Munich, Bavaria, Germany',
    'Founded': 'March 7, 1916',
    'Stock Information': {
        'Index': 'XETRA',
        'Date': 'Oct 03, 2022',
        'Open': 69.59,
        'High': 71.14,
        'Low': 68.61,
        'Close': 70.73,
        'Adj Close': 65.18,
        'Volume': 1062248,
        'LTP': 1111.65,
        'CHNG': -13.15,
        '%CHNG': -1.17,
        'TURNOVER': 246.06,
        '52 w-h': 1377.75,
        'Point Change': 34.79,
        '% Change': -4.73
    }
},
'Mercedes Benz Group AG': {
    'Industry': 'Automotive',
    'Website': 'https://www.mercedes-benz.com/',
    'Description': 'Mercedes-Benz Group AG is a German global automobile marque and a division of Daimler AG.',
    'Founders': 'Karl Benz and Gottlieb Daimler',
    'Headquarters': 'Stuttgart, Baden-Württemberg, Germany',
    'Founded': '1926',
    'Stock Information': {
        'Index': 'XETRA',
        'Date': 'Aug 30, 2022',
        'Open': 57.37,
        'High': 57.55,
        'Low': 56.6,
        'Close': 56.75,
        'Adj Close': 52.56,
        'Volume': 26100,
        'LTP': 2745.00,
        'CHNG': -122.75,
        '%CHNG': -4.28,
        'TURNOVER': 927.88,
        '52 w-h': 3021.10,
        'Point Change': 25.27,
        '% Change': -5.72
    }
},
'Adidas AG': {
    'Industry': 'Sportswear and Accessories',
    'Website': 'https://www.adidas-group.com/',
    'Description': 'Adidas AG is a German multinational corporation that designs and manufactures sports shoes, clothing, and accessories.',
    'Founders': 'Adolf Dassler',
    'Headquarters': 'Herzogenaurach, Bavaria, Germany',
    'Founded': 'August 18, 1949',
    'Stock Information': {
        'Index': 'XETRA',
        'Date': 'Dec 13, 2022',
        'Open': 66.7,
        'High': 67.15,
        'Low': 65.08,
        'Close': 65.44,
        'Adj Close': 65.16,
        'Volume': 141200,
        'LTP': 1489.50,
        'CHNG': -36.45,
        '%CHNG': -2.39,
        'TURNOVER': 1394.10,
        '52 w-h': 1725.00,
        'Point Change': 6.18,
        '% Change': -9.88
    }
},
'Vedanta Ltd': {
    'Industry': 'Mining and Metals',
    'Website': 'https://www.vedantalimited.com/',
    'Description': 'Vedanta Limited is a natural resources company engaged in exploring, extracting, and processing minerals and oil and gas.',
    'Founders': 'Anil Agarwal',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': '1976',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Jan 28, 2022',
        'Open': 330.9,
        'High': 335.9,
        'Low': 323.15,
        'Close': 327.65,
        'Adj Close': 213.34,
        'Volume': 15967353,
        'LTP': 669.75,
        'CHNG': -19.05,
        '%CHNG': -2.77,
        'TURNOVER': 151.4,
        '52 w-h': 775.65,
        'Point Change': 0.7,
        '% Change': -2.94
    }
},
'Alembic Ltd': {
    'Industry': 'Pharmaceuticals',
    'Website': 'https://www.alembicpharmaceuticals.com/',
    'Description': 'Alembic Limited is a pharmaceutical company that manufactures and markets a wide range of pharmaceutical products.',
    'Founders': 'Chirayu Amin',
    'Headquarters': 'Vadodara, Gujarat, India',
    'Founded': '1907',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Nov 09, 2022',
        'Open': 76.55,
        'High': 77.25,
        'Low': 75.9,
        'Close': 76.55,
        'Adj Close': 74.46,
        'Volume': 217318,
        'LTP': 2526.80,
        'CHNG': -67.9,
        '%CHNG': -2.62,
        'TURNOVER': 174.04,
        '52 w-h': 3629.05,
        'Point Change': -16.02,
        '% Change': -6.43
    }
},
'Meta Platforms Inc': {
    'Industry': 'Technology',
    'Website': 'https://about.fb.com/',
    'Description': 'Meta Platforms Inc., formerly known as Facebook, Inc., is an American technology conglomerate.',
    'Founders': 'Mark Zuckerberg, Andrew McCollum, Eduardo Saverin, Chris Hughes, and Dustin Moskovitz',
    'Headquarters': 'Menlo Park, California, USA',
    'Founded': 'February 4, 2004',
    'Stock Information': {
        'Index': 'NasdaqGS',
        'Date': 'Oct 24, 2022',
        'Open': 127.25,
        'High': 133.48,
        'Low': 124.57,
        'Close': 129.72,
        'Adj Close': 129.72,
        'Volume': 63563400,
        'LTP': 417.7,
        'CHNG': -29.35,
        '%CHNG': -6.57,
        'TURNOVER': 631.93,
        '52 w-h': 551.85,
        'Point Change': 86.93,
        '% Change': -14.06
    }
},
'Infosys Ltd': {
    'Industry': 'Information Technology Services',
    'Website': 'https://www.infosys.com/',
    'Description': 'Infosys Limited is an Indian multinational corporation that provides IT consulting and services.',
    'Founders': 'N. R. Narayana Murthy, Nandan Nilekani, S. Gopalakrishnan, S. D. Shibulal, K. Dinesh, N. S. Raghavan, and Ashok Arora',
    'Headquarters': 'Bengaluru, Karnataka, India',
    'Founded': 'July 2, 1981',
    'Stock Information': {
        'Index': 'NYSE',
        'Date': 'May 17, 2022',
        'Open': 1494.90,
        'High': 1525.00,
        'Low': 1480.90,
        'Close': 1518.45,
        'Adj Close': 1447.11,
        'Volume': 6516378,
        'LTP': 2340.90,
        'CHNG': -8.15,
        '%CHNG': -0.35,
        'TURNOVER': 572.85,
        '52 w-h': 2859.30,
        'Point Change': 9.6,
        '% Change': -3.94
    }
},
'IBM Common Stock': {
    'Industry': 'Information Technology Services',
    'Website': 'https://www.ibm.com/',
    'Description': 'International Business Machines Corporation (IBM) is an American multinational technology and consulting company.',
    'Founders': 'Charles Ranlett Flint',
    'Headquarters': 'Armonk, New York, USA',
    'Founded': 'June 16, 1911',
    'Stock Information': {
        'Index': 'NYSE',
        'Date': 'Jun 28, 2022',
        'Open': 142.92,
        'High': 144.16,
        'Low': 141.32,
        'Close': 141.86,
        'Adj Close': 133.39,
        'Volume': 4064800,
        'LTP': 720.45,
        'CHNG': -30.6,
        '%CHNG': -4.07,
        'TURNOVER': 1385.86,
        '52 w-h': 867,
        'Point Change': 52.41,
        '% Change': -13.14
    }
},
'Tata Consultancy Services Ltd': {
    'Industry': 'Information Technology Services',
    'Website': 'https://www.tcs.com/',
    'Description': 'Tata Consultancy Services (TCS) is an Indian multinational IT services and consulting company.',
    'Founders': 'Tata Group',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': 'April 1, 1968',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Nov 17, 2022',
        'Open': 3340.00,
        'High': 3360.00,
        'Low': 3317.75,
        'Close': 3349.00,
        'Adj Close': 3249.82,
        'Volume': 1417986,
        'LTP': 899.95,
        'CHNG': -59.35,
        '%CHNG': -6.19,
        'TURNOVER': 622.74,
        '52 w-h': 1242.00,
        'Point Change': 5.25,
        '% Change': -22.08
    }
},
'Hindustan Unilever Ltd': {
    'Industry': 'Consumer Goods',
    'Website': 'https://www.hul.co.in/',
    'Description': 'Hindustan Unilever Limited is a British-Dutch multinational consumer goods company.',
    'Founders': 'Lever Brothers',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': 'June 1933',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Sep 12, 2022',
        'Open': 2591.00,
        'High': 2605.00,
        'Low': 2574.00,
        'Close': 2580.40,
        'Adj Close': 2542.44,
        'Volume': 1595709,
        'LTP': 1689.55,
        'CHNG': -32.85,
        '%CHNG': -1.91,
        'TURNOVER': 764.67,
        '52 w-h': 1848.00,
        'Point Change': 51.44,
        '% Change': -0.83
    }
},
'Aditya Birla Money Ltd': {
    'Industry': 'Financial Services',
    'Website': 'https://www.adityabirlacapital.com/',
    'Description': 'Aditya Birla Money Limited is a financial services company that offers a range of solutions in equity and derivatives trading, currency derivatives, commodity trading, portfolio management, and more.',
    'Founders': 'Aditya Birla Group',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': '1995',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Mar 28, 2022',
        'Open': 61.5,
        'High': 61.5,
        'Low': 59.6,
        'Close': 59.8,
        'Adj Close': 59.815,
        'Volume': 59815,
        'LTP': 121.15,
        'CHNG': -4.5,
        '%CHNG': -3.58,
        'TURNOVER': 94.57,
        '52 w-h': 141.5,
        'Point Change': 41.28,
        '% Change': -7.87
    }
},
'Aditya Birla Capital Ltd': {
    'Industry': 'Financial Services',
    'Website': 'https://www.adityabirlacapital.com/',
    'Description': 'Aditya Birla Capital Limited is a financial services company providing a wide range of solutions, including insurance, asset management, private equity, and more.',
    'Founders': 'Aditya Birla Group',
    'Headquarters': 'Mumbai, Maharashtra, India',
    'Founded': '2007',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Jun 14, 2022',
        'Open': 94,
        'High': 97.3,
        'Low': 94,
        'Close': 94.95,
        'Adj Close': 94.95,
        'Volume': 2170914,
        'LTP': 223.6,
        'CHNG': -7.7,
        '%CHNG': -3.33,
        'TURNOVER': 610.54,
        '52 w-h': 265.3,
        'Point Change': 15.35,
        '% Change': -5.53
    }
},
'Sony Group Corp': {
    'Industry': 'Entertainment and Electronics',
    'Website': 'https://www.sony.net/',
    'Description': 'Sony Group Corporation is a Japanese multinational conglomerate corporation.',
    'Founders': 'Masaru Ibuka and Akio Morita',
    'Headquarters': 'Minato, Tokyo, Japan',
    'Founded': 'May 7, 1946',
    'Stock Information': {
        'Index': 'NYSE',
        'Date': 'Oct 17, 2022',
        'Open': 65.07,
        'High': 66.34,
        'Low': 65.07,
        'Close': 66.09,
        'Adj Close': 66.09,
        'Volume': 897500,
        'LTP': 630,
        'CHNG': -50.9,
        '%CHNG': -7.48,
        'TURNOVER': 574.61,
        '52 w-h': 776.5,
        'Point Change': 86.25,
        '% Change': -9.27
    }
},
'Maruti Suzuki India Ltd': {
    'Industry': 'Automotive',
    'Website': 'https://www.marutisuzuki.com/',
    'Description': 'Maruti Suzuki India Limited is an Indian subsidiary of Japanese automaker Suzuki Motor Corporation.',
    'Founders': 'Government of India and Suzuki Motor Corporation',
    'Headquarters': 'New Delhi, India',
    'Founded': 'February 24, 1981',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Jul 01, 2022',
        'Open': 8440.00,
        'High': 8450.00,
        'Low': 8305.60,
        'Close': 8402.60,
        'Adj Close': 8269.82,
        'Volume': 530569,
        'LTP': 1960.00,
        'CHNG': -75.1,
        '%CHNG': -3.69,
        'TURNOVER': 522.52,
        '52 w-h': 2253.00,
        'Point Change': 5.24,
        '% Change': -11.35
    }
},
'Hero Motocorp Ltd': {
    'Industry': 'Automotive',
    'Website': 'https://www.heromotocorp.com/',
    'Description': 'Hero MotoCorp Limited is an Indian multinational motorcycle and scooter manufacturer.',
    'Founders': 'Brijmohan Lall Munjal',
    'Headquarters': 'New Delhi, India',
    'Founded': 'January 19, 1984',
    'Stock Information': {
        'Index': 'NSE',
        'Date': 'Apr 13, 2022',
        'Open': 2291.55,
        'High': 2311.15,
        'Low': 2268.90,
        'Close': 2274.40,
        'Adj Close': 2137.30,
        'Volume': 426929,
        'LTP': 1781.00,
        'CHNG': -68.9,
        '%CHNG': -3.72
    }
}
}

def view_company_info():
    company_name = input("Enter the company name to view information: ")
    company_name = company_name.strip()

    if company_name in company_info:
        info = company_info[company_name]
        print(f"\nCompany: {company_name}")
        print(f"Industry: {info['Industry']}")
        print(f"Website: {info['Website']}")
        print(f"Description: {info['Description']}")
        print(f"Founders: {info['Founders']}")
        print(f"Headquarters: {info['Headquarters']}")
        print(f"Founded: {info['Founded']}")
    else:
        print("Company not found. Please check the company name.")

def main():
    root = Tk()
    root.withdraw()

    file_path = "/home/almightynan/Downloads/mayhem/jeya_suryaa/stock analysis.csv"

    if not file_path:
        print(RED + "No file selected. Exiting..." + RESET)
        return

    df = load_data(file_path)
    numDf = load_data("/home/almightynan/Downloads/mayhem/jeya_suryaa/numerical_stockData.csv")

    if df is None:
        return

    options = [
        BOLD + "Analyze Open Column" + RESET,                           #1
        BOLD + "Analyze High Column" + RESET,                           #2
        BOLD + "Analyze Low Column" + RESET,                            #3
        BOLD + "Export Data as CSV" + RESET,                            #4
        BOLD + "Plot Line Graph" + RESET,                               #5
        BOLD + "Plot Bar Graph" + RESET,                                #6
        BOLD + "Predict future values via linear regression" + BOLD,    #7
        BOLD + "View Company Information" + RESET,                      #8
        BOLD + "Quit" + RESET,                                          #9
    ]

    while True:
        if sys.platform.startswith('win'):
            os.system('cls')  # Windows
        else:
            os.system('clear')  # Linux or MacOS
        table = PrettyTable()
        table.field_names = [BOLD + GREEN + "Option" + RESET, BOLD + "Description" + RESET]
        
        for i, option in enumerate(options, start=1):
            table.add_row([GREEN + f"{i}" + RESET, option])

        print(table)

        choice = input(f"{YELLOW} => {RESET}{BOLD} Select an option (1-9):{RESET} ")

        if choice == "1":
            analyze_column_stats(df, "Open")
        elif choice == "2":
            analyze_column_stats(df, "High")
        elif choice == "3":
            analyze_column_stats(df, "Low")
        elif choice == "4":
            export_data_to_csv(df)
        elif choice == "5":
            plot_line_graph(
                df,
                ["Open", "High", "Low", "Close", "Adj Close", "Volume"],
                "Line Graph",
            )
        elif choice == "6":
            plot_bar_graph(
                df, ["LTP", "CHNG", "%CHNG", "TURNOVER", "52 w-h"], "Bar Graph"
            )
        elif choice == "7":
            target_column = input("Enter the target column to predict (e.g., High, Low, Close, Adj Close, Volume, TURNOVER, Point Change, % Change): ")
            feature_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'TURNOVER', 'Point Change', '% Change']

            if target_column in df.columns and all(col in numDf.columns for col in feature_columns):
                prediction_model = train_linear_regression_model(numDf, target_column, feature_columns)
                future_features = np.array([[2300.0, 2350.0, 2250.0, 2400.0, 2380.0, 8000000, 500, -10.0, -1.0]])
                future_prediction = predict_future_values(prediction_model, feature_columns, future_features)
                print(f'Predicted Future {target_column}: {future_prediction}')
            else:
                print("Invalid target or feature columns.")

        elif choice == "8":
            view_company_info()
        elif choice == "9":
            break
        else:
            print(RED + "Invalid choice. Please select a valid option." + RESET)
            print(YELLOW + "This screen will clear shortly." + RESET)
            time.sleep(3)
            os.system('cls' if sys.platform.startswith('win') else 'clear')

if __name__ == "__main__":
    main()
