import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
import matplotlib.dates as mdates

# Read the CSV file
s = pd.read_csv("stock analysis.csv")

# Create a Tkinter window
root = tk.Tk()
root.title("Stock Analysis App")
root.geometry("800x600")  # Set the window size

# Create a Notebook widget to manage different tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH)

# Create tabs for different functionalities
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

notebook.add(tab1, text="View Data")
notebook.add(tab2, text="Plot Graph")
notebook.add(tab3, text="Filtered Data")
notebook.add(tab4, text="Stock Analysis")


# Function to view data for all companies
def view_data():
    # Create a Treeview widget to display data
    tree = ttk.Treeview(tab1)
    tree["columns"] = tuple(s.columns)
    tree.heading("#0", text="idx")
    for col in s.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for index, row in s.iterrows():
        tree.insert("", "end", text=index, values=tuple(row))
    tree.pack(fill=tk.BOTH)


# Create a frame for the Treeview in tab1
treeview_frame = ttk.Frame(tab1)
treeview_frame.pack(fill=tk.BOTH)

# Create a frame for the Excel-like display in tab3
excel_frame = ttk.Frame(tab3)
excel_frame.pack(fill=tk.BOTH)


# Function to extract and plot numerical data
def plot_graph():
    selected_company = company_var.get()
    if selected_company:
        company_data = s[s["idx"] == selected_company]
        date_column = pd.to_datetime(
            company_data["Date"], format="%b %d, %Y"
        )  # Convert date strings to datetime objects

        # Specify the numerical columns you want to plot
        numerical_columns = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
            "LTP",
            "TURNOVER",
            "52 w-h",
        ]

        # Create a bar graph with each numerical column as a separate bar
        plt.figure(figsize=(12, 8))  # Adjust the figure size as needed

        for i, col in enumerate(numerical_columns):
            x = date_column + pd.DateOffset(
                days=i
            )  # Offset the x-axis position for each bar
            plt.bar(x, company_data[col], width=0.1, label=col)

        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter("%b %d, %Y")
        )  # Format the x-axis date labels
        plt.title(f"{selected_company} Stock Data")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability
        plt.legend(loc="best", fontsize="small")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# Function to display filtered data in an Excel-like sheet
def display_filtered_data():
    # Clear existing widgets in the excel_frame
    for widget in excel_frame.winfo_children():
        widget.destroy()

    selected_column = column_var.get()
    if selected_column:
        filtered_data = s[[selected_column]]

        # Create a Treeview widget to display filtered data in the Excel-like frame
        tree = ttk.Treeview(excel_frame)
        tree["columns"] = (selected_column,)
        tree.heading("#0", text="Index")
        tree.heading(selected_column, text=selected_column)
        tree.column("#0", width=100)
        tree.column(selected_column, width=100)

        for index, value in filtered_data.iterrows():
            tree.insert("", "end", text=index, values=(value[selected_column],))

        tree.pack(fill=tk.BOTH)


# Function to perform stock analysis
def stock_analysis():
    selected_company = stock_company_var.get()
    if selected_company:
        # Filter the data for the selected company
        company_data = s[s["idx"] == selected_company]
        # Calculate the average closing price (assuming 'Close' is the column)
        avg_close_price = company_data["Close"].mean()
        # Display the result using a messagebox or any other suitable method
        result_label.config(
            text=f"Average Closing Price for {selected_company}: {avg_close_price:.2f}"
        )


# Create widgets for each tab
# Tab 1 - View Data
view_data_button = tk.Button(tab1, text="View Data", command=view_data)
view_data_button.pack()

# Tab 2 - Plot Graph
# Create a frame for the Select Company label and dropdown in the center
company_frame = ttk.Frame(tab2)
company_frame.pack(fill=tk.BOTH)  # Adjust padding as needed

company_label = tk.Label(company_frame, text="Select Company:")
company_label.pack()

company_var = tk.StringVar()
company_dropdown = ttk.Combobox(
    company_frame, textvariable=company_var, values=s["idx"].tolist()
)
company_dropdown.pack()

# Create a frame for the Plot Graph button in the center
button_frame = ttk.Frame(tab2)
button_frame.pack(fill=tk.BOTH)  # Adjust padding as needed

plot_button = tk.Button(button_frame, text="Plot Graph", command=plot_graph)
plot_button.config(width=30, height=2)  # Increase button size
plot_button.pack()

# Tab 3 - Filtered Data
# Create a frame for the Select Column label and dropdown in the center
column_frame = ttk.Frame(tab3)
column_frame.pack(fill=tk.BOTH)  # Adjust padding as needed

column_label = tk.Label(column_frame, text="Select Column:")
column_label.pack()

column_var = tk.StringVar()
column_dropdown = ttk.Combobox(
    column_frame, textvariable=column_var, values=s.columns.tolist()
)
column_dropdown.pack()

# Create a frame for the Display Filtered Data button in the center
button_frame = ttk.Frame(tab3)
button_frame.pack(fill=tk.BOTH)  # Adjust padding as needed

display_button = tk.Button(
    button_frame, text="Display Filtered Data", command=display_filtered_data
)
display_button.config(width=30, height=2)  # Increase button size
display_button.pack()

# Tab 4 - Stock Analysis
result_label = tk.Label(tab4, text="")
stock_company_label = tk.Label(tab4, text="Select Company:")
stock_company_var = tk.StringVar()
stock_company_dropdown = ttk.Combobox(
    tab4, textvariable=stock_company_var, values=s["idx"].tolist()
)
stock_analysis_button = tk.Button(
    tab4, text="Perform Stock Analysis", command=stock_analysis
)
stock_analysis_button.config(width=30, height=2)  # Increase button size

result_label.pack()
stock_company_label.pack()
stock_company_dropdown.pack()
stock_analysis_button.pack()

root.mainloop()
