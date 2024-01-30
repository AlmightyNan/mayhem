import mysql.connector as msc
import numpy as np
import connectors.config as config
from prettytable import PrettyTable
from src.utils import CustomLogger as logger
from connectors.init import Initialize
from connectors.insert import Insert
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Button, Combobox
import threading
from tkinter.simpledialog import askinteger
import pandas as pd
from prettytable import PrettyTable
from tkinter import StringVar
from tkinter import ttk, font
import matplotlib.pyplot as plt
from tkinter import filedialog
from sqlalchemy import create_engine
import math

def center_window(window):
    window.update_idletasks()  # Make sure window size is updated
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def show_credits():
    title_label.config(text="Credits", font=("Montserrat", 16, "bold"))
    label.config(
        text="<placeholder>",
        font=("Montserrat", 12),
    )
    enter_button.pack_forget()
    exit_button.pack_forget()
    credits_button.pack_forget()
    view_all_data.pack_forget()
    go_back_button.pack(
        side=tk.LEFT, padx=10, pady=10
    )  # Adding spacing on the left side and at the top


def go_back_to_main_menu():
    center_window(root)
    title_label.config(text="Welcome", font=("Montserrat", 16, "bold"))
    label.config(
        text="Please choose an option below to initiate the desired action.",
        font=("Montserrat", 12),
    )
    go_back_button.pack_forget()
    option1.pack_forget()
    option2.pack_forget()
    option3.pack_forget()
    option4.pack_forget()
    option5.pack_forget()
    # credits_button.pack_forget()
    return_to_main_menu.pack_forget()
    enter_button.pack(side=tk.LEFT, padx=10)
    exit_button.pack(side=tk.RIGHT, padx=10)
    view_all_data.pack(side=tk.LEFT, padx=10)
    credits_button.pack(
        side=tk.LEFT, padx=10
    )  # Change this to left to align with other buttons


def show_head_tail():
    center_window(root)
    num_rows_head = askinteger(
        "Input", "Enter the number of rows to select from top:", parent=root
    )
    num_rows_tail = askinteger(
        "Input", "Enter the number of rows to select from bottom:", parent=root
    )

    if (
        num_rows_head is not None
        and num_rows_head > 0
        and num_rows_tail is not None
        and num_rows_tail > 0
    ):
        data = pd.read_csv("datasets/colleges.csv")
        top_rows = data.head(num_rows_head)
        bottom_rows = data.tail(num_rows_tail)

        # Trim columns that are longer than 300 characters
        columns_to_trim = ["Courses", "Facilities"]
        for col in columns_to_trim:
            top_rows.loc[:, col] = top_rows[col].apply(
                lambda x: x[:300] if isinstance(x, str) and len(x) > 300 else x
            )
            bottom_rows.loc[:, col] = bottom_rows[col].apply(
                lambda x: x[:300] if isinstance(x, str) and len(x) > 300 else x
            )

        def update_display():
            selected_col = selected_column.get()

            top_text = top_rows[selected_col].to_string(index=True)
            bottom_text = bottom_rows[selected_col].to_string(index=True)

            result_text.config(state=tk.NORMAL)  # Enable the Text widget
            result_text.delete(1.0, tk.END)
            result_text.insert(
                tk.END,
                f"Top {num_rows_head} Rows:\n{top_text}\n\nBottom {num_rows_tail} Rows:\n{bottom_text}",
            )
            result_text.config(state=tk.DISABLED)  # Disable the Text widget again

        result_window = tk.Toplevel(root)
        result_window.title("Head and Tail")
        result_window.geometry("800x600")
        center_window(root)

        # Create a dropdown menu for column selection
        selected_column = tk.StringVar()
        selected_column.set(
            top_rows.columns[0]
        )  # Set default value to the first column
        column_dropdown = ttk.Combobox(
            result_window,
            textvariable=selected_column,
            values=top_rows.columns.tolist(),
        )
        column_dropdown.pack(pady=10)

        result_text = tk.Text(result_window, wrap=tk.WORD, font=("Montserrat", 12))
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        update_button = ttk.Button(result_window, text="Update", command=update_display)
        update_button.pack(pady=5)

        update_display()  # Initial display


# Rest of your code...


def on_exit():
    root.destroy()


animation_running = True


def on_enter_button_click():
    center_window(root)

    def update_text_animation(dot_count):
        global animation_running
        if animation_running:
            if dot_count == 0:
                label.config(
                    text="Data Insertion in Progress, Kindly await completion.",
                    font=("Montserrat", 12),
                )
                # Disable the buttons when the animation starts
                enter_button.config(state=tk.DISABLED)
                exit_button.config(state=tk.DISABLED)
            else:
                current_text = label.cget("text")
                label.config(text=current_text + ".", font=("Montserrat", 12))
            dot_count = (dot_count + 1) % 4
            root.after(1000, update_text_animation, dot_count)
        else:
            # Enable the buttons after the text is updated
            enter_button.config(state=tk.NORMAL)
            exit_button.config(state=tk.NORMAL)

    def finish_inserting_data():
        global animation_running
        animation_running = False
        title_label.config(text="Database Initialization Complete")
        label.config(
            text="Please utilize the provided buttons to commence the process.",
            font=("Montserrat", 12),
        )
        # Enable the buttons after the text is updated
        view_all_data.pack_forget()
        enter_button.config(state=tk.NORMAL, command=search_dataset)
        exit_button.config(state=tk.NORMAL)

    def initialize_and_insert_data():
        # connection = mydb.cursor()
        # Initialize.db(connection)
        # Insert.from_csv(connection, "./datasets/movies.csv")
        finish_inserting_data()

    # Start the animation thread
    animation_thread = threading.Thread(target=update_text_animation, args=(0,))
    animation_thread.start()

    # Start the initialization thread
    initialize_thread = threading.Thread(target=initialize_and_insert_data)
    initialize_thread.start()

    # Remove the "Credits" button when the "Enter" button is clicked
    credits_button.pack_forget()


def show_csv_data():
    center_window(root)
    csv_file_path = "datasets/colleges.csv"  # Update with your actual CSV file path
    page_size = 50  # Number of rows per page

    def load_data(page_num):
        center_window(root)
        start_idx = page_num * page_size
        end_idx = start_idx + page_size

        data = pd.read_csv(csv_file_path)
        page_data = data.iloc[start_idx:end_idx]

        return page_data

    def show_page(page_num):
        center_window(root)
        nonlocal current_page  # Use nonlocal to update the outer current_page variable
        current_page = page_num  # Update the current_page variable

        tree.delete(*tree.get_children())  # Clear existing data in the Treeview
        page_data = load_data(page_num)

        for index, row in page_data.iterrows():
            tree.insert("", "end", values=row.tolist())

    result_window = tk.Toplevel(root)
    result_window.title("CSV Data")
    result_window.geometry("1000x800")
    center_window(root)
    data = pd.read_csv(csv_file_path)  # Load the data here
    column_display_names = [
        "College Name",
        "Genders Accepted",
        "Campus Size",
        "Total Student Enrollments",
        "Total Faculty",
        "Established Year",
        "Rating",
        "University",
        "Courses",
        "Facilities",
        "City",
        "State",
        "Country",
        "College Type",
        "Average Fees",
    ]

    # tree = ttk.Treeview(result_window, columns=column_display_names, show="headings")
    # tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.configure(
        "Treeview.Heading", font=("Helvetica", 12)
    )  # Change font and size as needed

    # Create the Treeview widget with the custom style
    tree = ttk.Treeview(
        result_window,
        columns=column_display_names,
        show="headings",
        style="Custom.Treeview",
    )
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for col in column_display_names:
        tree.heading(col, text=col)  # Set heading text to column name
        tree.column(col, width=100)  # Adjust column width as needed

    prev_page_button = ttk.Button(
        result_window,
        text="Previous Page",
        style="PrevPage.TButton",
        command=lambda: show_page(current_page - 1),
    )
    prev_page_button.pack(side=tk.LEFT, padx=10)

    prev_page_button_style = ttk.Style()
    prev_page_button_style.configure(
        "PrevPage.TButton", font=("Helvetica", 15)
    )  # Change font and size as needed

    next_page_button = ttk.Button(
        result_window,
        text="Next Page",
        style="NextPage.TButton",
        command=lambda: show_page(current_page + 1),
    )
    next_page_button.pack(side=tk.RIGHT, padx=10)

    prev_page_button_style = ttk.Style()
    prev_page_button_style.configure(
        "NextPage.TButton", font=("Helvetica", 15)
    )  # Change font and size as needed

    current_page = 0
    show_page(current_page)


def search_and_compare():
    search_query = search_entry.get().strip()
    if search_query:
        # Find the most related college name
        related_college = data[
            data["College Name"].str.contains(search_query, case=False, na=False)
        ].iloc[0]
        college_name = related_college["College Name"]
        compare_colleges(college_name, selected_college)
    else:
        messagebox.showinfo("Search Error", "Please enter a search query.")


def search_dataset():
    """
    Function to search the dataset and display options for further actions.
    """
    center_window(root)
    title_label.config(
        text="Please make a selection to proceed.", font=("Montserrat", 16, "bold")
    )
    enter_button.pack_forget()
    label.config(
        text="Option 1 - View top x and bottom y rows.\nOption 2 - Export certain rows from dataset.\nOption 3 - Compare data between 2 colleges.\nOption 4 - View a brief info about a college\nOption 5 - Display college ratings.",
    )
    option1.pack(side=tk.LEFT, padx=10)
    option2.pack(side=tk.LEFT, padx=10)
    option3.pack(side=tk.LEFT, padx=10)
    option4.pack(side=tk.LEFT, padx=10)
    option5.pack(side=tk.LEFT, padx=10)
    credits_button.pack_forget()
    view_all_data.pack_forget()
    return_to_main_menu.pack(side=tk.LEFT, padx=10)
    exit_button.pack_forget()


def compare_colleges(college1, college2):
    try:
        # Load the data
        data = pd.read_csv("datasets/colleges.csv")

        # Filter data for the entered college names
        college1_data = data[data["College Name"].str.contains(college1, case=False)]
        college2_data = data[data["College Name"].str.contains(college2, case=False)]

        # Check if data is found for both colleges
        if college1_data.empty or college2_data.empty:
            messagebox.showinfo(
                "Error", "One or both college names not found in the data."
            )
            return

        # Columns to compare
        columns_to_compare = [
            "Campus Size",
            "Average Fees",
            "Total Student Enrollments",
        ]

        # Convert Campus Size values to int after handling different cases
        college1_data.loc[:, "Campus Size"] = college1_data["Campus Size"].apply(
            parse_campus_size
        )
        college2_data.loc[:, "Campus Size"] = college2_data["Campus Size"].apply(
            parse_campus_size
        )

        # Handle NaN values by replacing them with 0
        college1_data[columns_to_compare] = college1_data[columns_to_compare].fillna(0)
        college2_data[columns_to_compare] = college2_data[columns_to_compare].fillna(0)

        # Convert values to float for comparison
        values_college1 = college1_data[columns_to_compare].values[0].astype(float)
        values_college2 = college2_data[columns_to_compare].values[0].astype(float)

        # Compare the length of courses
        courses_college1 = college1_data["Courses"].str.split(", ").dropna().iloc[0]
        courses_college2 = college2_data["Courses"].str.split(", ").dropna().iloc[0]

        courses_length_college1 = len(courses_college1)
        courses_length_college2 = len(courses_college2)

        courses_comparison = {
            college1: courses_length_college1,
            college2: courses_length_college2,
        }

        # Create bar graphs for comparison with custom colors
        plt.figure(figsize=(10, 5))

        # Specify custom colors for the bars
        colors = ["#050100", "#9000ff"]

        plt.subplot(2, 2, 1)
        plt.bar(
            list(courses_comparison.keys()),
            list(courses_comparison.values()),
            color=colors,
        )
        plt.xlabel("Colleges")
        plt.ylabel("Number of Courses")
        plt.title("Number of Courses Comparison")
        plt.xticks(rotation=45, ha="right")
        # plt.annotate(
        #     college1,
        #     (0, courses_length_college1),
        #     textcoords="offset points",
        #     xytext=(0, 10),
        #     ha="center",
        # )
        # plt.annotate(
        #     college2,
        #     (1, courses_length_college2),
        #     textcoords="offset points",
        #     xytext=(0, 10),
        #     ha="center",
        # )

        plt.subplot(2, 2, 2)
        plt.bar(
            [college1, college2],
            [values_college1[0], values_college2[0]],
            color=["#050100", "#9000ff"],
        )
        plt.xlabel("Colleges")
        plt.ylabel("Campus Size")
        plt.title("Campus Size Comparison")
        plt.xticks(rotation=45, ha="right")

        plt.subplot(2, 2, 3)
        avg_fees_college1 = college1_data["Average Fees"].values[0]
        avg_fees_college2 = college2_data["Average Fees"].values[0]

        plt.bar(
            [college1, college2], [avg_fees_college1, avg_fees_college2], color=colors
        )
        plt.xlabel("Colleges")
        plt.ylabel("Average Fees")
        plt.title("Average Fees Comparison")
        plt.xticks(rotation=45, ha="right")

        plt.subplot(2, 2, 4)
        enrollments_college1 = college1_data["Total Student Enrollments"].values[0]
        enrollments_college2 = college2_data["Total Student Enrollments"].values[0]

        plt.bar(
            [college1, college2],
            [enrollments_college1, enrollments_college2],
            color=colors,
        )
        plt.xlabel("Colleges")
        plt.ylabel("Total Student Enrollments")
        plt.title("Total Student Enrollments Comparison")
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        plt.show()

    except Exception as e:
        messagebox.showinfo("Error", f"An error occurred: {e}")
        print(e)


def parse_campus_size(value):
    try:
        # Handle cases where value is not in the expected format
        if isinstance(value, str) and "Acre" in value:
            return float(value.replace(" Acres", ""))
        elif isinstance(value, str) and value.isdigit():
            return float(value)
        else:
            return 0.0
    except:
        return 0.0


def export_csv_data():
    global data  # Make sure data is a global variable accessible in this function
    data = pd.read_csv(
        "/home/almightynan/Desktop/mayhem/mayhem/datasets/colleges.csv"
    )  # Load your CSV data here

    def load_data(page_num):
        start_idx = page_num * page_size
        end_idx = start_idx + page_size

        return data.iloc[start_idx:end_idx]

    def show_page(page_num):
        nonlocal current_page  # Use nonlocal to update the outer current_page variable
        current_page = page_num

        tree.delete(*tree.get_children())  # Clear existing data in the Treeview
        page_data = load_data(page_num)

        for index, row in page_data.iterrows():
            tree.insert("", "end", values=row.tolist())

    def prev_page():
        if current_page > 0:
            show_page(current_page - 1)

    def next_page():
        last_page = (len(data) - 1) // page_size
        if current_page < last_page:
            show_page(current_page + 1)

    def save_changes():
        updated_data = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            updated_data.append(values)

        # Convert the updated data back to a DataFrame
        updated_df = pd.DataFrame(updated_data, columns=data.columns)

        # Define supported file extensions
        supported_extensions = ["csv", "xlsx", "json", "html"]

        # Create a Combobox for selecting the file extension
        file_extension_combo = Combobox(
            root, values=supported_extensions, state="readonly"
        )
        file_extension_combo.set("csv")
        file_extension_combo.pack()

        def save_with_extension():
            user_extension = file_extension_combo.get().lower()

            if user_extension not in supported_extensions:
                messagebox.showerror("Invalid Extension", "Unsupported file extension.")
                return

            # Prompt the user to select a file location to save the updated data
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{user_extension}",
                filetypes=[
                    ("CSV Files", "*.csv"),
                    ("Excel Files", "*.xlsx"),
                    ("JSON Files", "*.json"),
                    ("HTML Files", "*.html"),
                ],
            )

            if file_path:
                if user_extension == "csv":
                    updated_df.to_csv(file_path, index=False)
                elif user_extension == "xlsx":
                    updated_df.to_excel(file_path, index=False)
                elif user_extension == "json":
                    updated_df.to_json(file_path, orient="records")
                elif user_extension == "html":
                    updated_df.to_html(file_path, index=False)

                messagebox.showinfo(
                    "Save Successful", f"Changes saved to '{file_path}'."
                )

        # # Create a button to trigger the save process
        # save_button = tk.Button(root, text="Save Changes", command=save_with_extension)
        # save_button.pack()

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit CSV Data")
        edit_window.geometry("1000x800")
        center_window(edit_window)

        page_size = 10  # Number of rows per page
        current_page = 0

        column_display_names = data.columns

        # Create the Treeview widget with the custom style
        tree = ttk.Treeview(
            edit_window,
            columns=column_display_names,
            show="headings",
            style="Custom.Treeview",
        )
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col_index, col in enumerate(column_display_names):
            tree.heading(col_index, text=col)  # Set the heading text using the index
            tree.column(col_index, width=100)  # Adjust column width as needed

        entry_widgets = {}  # Store entry widgets for each row

        for index, row in load_data(current_page).iterrows():
            item = tree.insert("", "end", values=row.tolist())
            entry_widgets[item] = []

            for col_index, col_value in enumerate(row):
                entry = tk.Entry(tree, justify="center", font=("Helvetica", 12))
                entry.insert(0, col_value)
                tree.window_create(item, col_index, window=entry)
                entry_widgets[item].append(entry)

        prev_page_button = ttk.Button(
            edit_window, text="Previous Page", command=prev_page
        )
        prev_page_button.pack(side=tk.LEFT, padx=10)

        next_page_button = ttk.Button(edit_window, text="Next Page", command=next_page)
        next_page_button.pack(side=tk.RIGHT, padx=10)

        save_button = ttk.Button(
            edit_window,
            text="Save this data to a CSV",
            command=save_changes,
            style="Montserrat.TButton",
        )
        save_button.pack(pady=10)

        # Define a custom style for the buttons to use Montserrat font
        style = ttk.Style()
        style.configure(
            "Custom.Treeview", font=("Helvetica", 12)
        )  # Change font and size as needed
        style.configure("Montserrat.TButton", font=("Montserrat", 12))

    def finish_editing(event, item, row, col):
        new_value = entry_var.get()
        tree.item(item, values=("", new_value, ""))
        entry.place_forget()
        entry.unbind("<FocusOut>")

    def save_changes():
        updated_data = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            updated_data.append(values)

        # Convert the updated data back to a DataFrame
        updated_df = pd.DataFrame(updated_data, columns=data.columns)

        # Define supported file extensions
        supported_extensions = ["csv", "xlsx", "json", "html"]

        def save_with_extension():
            user_extension = file_extension_combo.get().lower()

            if user_extension not in supported_extensions:
                messagebox.showerror("Invalid Extension", "Unsupported file extension.")
                return

            # Prompt the user to select a file location to save the updated data
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{user_extension}",
            )

            if file_path:
                if user_extension == "csv":
                    updated_df.to_csv(file_path, index=False)
                elif user_extension == "xlsx":
                    updated_df.to_excel(file_path, index=False)
                elif user_extension == "json":
                    updated_df.to_json(file_path, orient="records")
                elif user_extension == "html":
                    updated_df.to_html(file_path, index=False)

                messagebox.showinfo(
                    "Save Successful", f"Changes saved to '{file_path}'."
                )
                extension_button.pack_forget()

        def open_extension_selector():
            extension_window = tk.Toplevel(root)
            extension_window.title("Select File Extension")

            # Create a Combobox for selecting the file extension
            file_extension_combo = ttk.Combobox(
                extension_window, values=supported_extensions, state="readonly"
            )
            file_extension_combo.set("csv")
            file_extension_combo.pack(padx=10, pady=10)

            # Create a button to trigger the save process with the selected extension
            save_button = tk.Button(
                extension_window, text="Save Changes", command=save_with_extension
            )
            save_button.pack(pady=10)
            extension_button.pack_forget()

        # Create a button to open the extension selector window
        extension_button = tk.Button(
            root, text="Select File Extension", command=open_extension_selector
        )
        extension_button.pack(pady=10)
        extension_button.pack_forget()
        # Create a new Toplevel window for the file extension selection
        extension_window = tk.Toplevel(edit_window)
        extension_window.title("Select an extension")
        extension_window.geometry("600x300")
        center_window(extension_window)

        # Create a Combobox for selecting the file extension
        file_extension_combo = ttk.Combobox(
            extension_window, values=supported_extensions, state="readonly"
        )
        file_extension_combo.set("csv")
        file_extension_combo.pack(padx=10, pady=10)

        # Create a button to trigger the save process with the selected extension
        save_button = tk.Button(
            extension_window, text="Save Changes", command=save_with_extension
        )
        save_button.pack(pady=10)

        # Create a button to open the extension selector window
        extension_button = tk.Button(
            root, text="Select File Extension", command=open_extension_selector
        )
        extension_button.pack(pady=10)
        extension_button.pack_forget()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit CSV Data")
    edit_window.geometry("1000x800")
    center_window(edit_window)

    page_size = 50  # Number of rows per page
    current_page = 0

    column_display_names = data.columns

    # Create the Treeview widget with the custom style
    tree = ttk.Treeview(
        edit_window,
        columns=column_display_names,
        show="headings",
        style="Custom.Treeview",
    )
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree.heading("#1", text="Column A")
    tree.heading("#2", text="Column B")
    tree.heading("#3", text="Column C")

    tree.insert("", "end", values=("Value 1", "Value 2", "Value 3"))

    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var)

    entry_var = tk.StringVar()
    entry = tk.Entry(edit_window, textvariable=entry_var)

    # Set the heading text for columns based on column_display_names
    for col_index, col in enumerate(column_display_names):
        tree.heading(col_index, text=col)  # Set the heading text using the index
        tree.column(col_index, width=100)  # Adjust column width as needed

    prev_page_button = ttk.Button(edit_window, text="Previous Page", command=prev_page)
    prev_page_button.pack(side=tk.LEFT, padx=10)

    next_page_button = ttk.Button(edit_window, text="Next Page", command=next_page)
    next_page_button.pack(side=tk.RIGHT, padx=10)

    save_button = ttk.Button(
        edit_window,
        text="Save this page in a custom extension",
        command=save_changes,
        style="Montserrat.TButton",
    )
    save_button.pack(pady=10)

    # Define a custom style for the buttons to use Montserrat font
    style = ttk.Style()
    style.configure(
        "Custom.Treeview", font=("Helvetica", 12)
    )  # Change font and size as needed
    style.configure("Montserrat.TButton", font=("Montserrat", 12))

    # Initially show the first page
    show_page(current_page)


def compare_colleges_window():
    def compare():
        college1 = college1_var.get().strip()
        college2 = college2_var.get().strip()

        if college1 and college2:
            compare_colleges(college1, college2)
        else:
            messagebox.showinfo("Input Error", "Please enter both college names.")

    compare_window = tk.Toplevel(root)
    compare_window.title("Compare Colleges")
    compare_window.geometry("400x250")
    center_window(compare_window)

    college1_label = tk.Label(compare_window, text="Enter College 1:")
    college1_label.pack(pady=10)
    college1_var = tk.StringVar()
    college1_entry = tk.Entry(compare_window, textvariable=college1_var)
    college1_entry.pack()

    college2_label = tk.Label(compare_window, text="Enter College 2:")
    college2_label.pack(pady=10)
    college2_var = tk.StringVar()
    college2_entry = tk.Entry(compare_window, textvariable=college2_var)
    college2_entry.pack()

    compare_button = tk.Button(compare_window, text="Compare", command=compare)
    compare_button.pack(pady=10)


def search_college():
    college_name = simpledialog.askstring("Search College", "Enter College Name:")
    if college_name:
        # Use a case-insensitive search for college names
        data = pd.read_csv("datasets/colleges.csv")
        relevant_data = data[
            data["College Name"].str.contains(college_name, case=False)
        ]
        if not relevant_data.empty:
            display_results_window(relevant_data.iloc[0])
        else:
            messagebox.showinfo("No Results", "No matching data found.")


def calculate_rating(established_year, total_student_enrollments, total_faculty, average_fees):
    # Convert established_year to integer if it's not NaN and not 'Established Year'
    if established_year != 'Established Year' and not pd.isnull(established_year):
        established_year = int(established_year)
    else:
        established_year = 0
    
    # Convert other values to integers or floats if they are not NaN
    try:
        total_faculty = int(total_faculty) if not pd.isnull(total_faculty) else 0
        total_student_enrollments = int(total_student_enrollments) if not pd.isnull(total_student_enrollments) else 0
        average_fees = float(average_fees) if not pd.isnull(average_fees) else 0
    except ValueError:
        total_faculty = 0
        total_student_enrollments = 0
        average_fees = 0
    
    # Weightage factors for each criterion
    established_year_weight = 0.2
    student_faculty_ratio_weight = 0.3
    average_fees_weight = 0.3
    campus_size_weight = 0.2

    # Adjust established year to give more weightage to older colleges
    adjusted_established_year = max(established_year - 1900, 0)

    # Calculate rating based on weighted factors
    try:
        rating = (
            (adjusted_established_year * established_year_weight) +
            ((total_faculty / total_student_enrollments) * student_faculty_ratio_weight) +
            ((1 / average_fees) * average_fees_weight) +
            (campus_size_weight / np.sqrt(total_student_enrollments))  # Adjust for campus size
        )
    except ZeroDivisionError:
        rating = 0  # Handle division by zero
    
    # Scale rating between 0 and 5
    scaled_rating = min(max(rating / 5, 0), 5)
    
    return f"{scaled_rating:.2f}/5"

def open_college_ratings_window():
    # Create a new window for displaying college ratings
    ratings_window = tk.Toplevel(root)
    ratings_window.title("College Ratings")
    
    # Create a DataFrame to hold the data
    data = pd.read_csv("./datasets/colleges.csv")
    
    # Calculate ratings for each college
    data['Rating'] = data.apply(lambda row: calculate_rating(row['Established Year'], row['Total Student Enrollments'], row['Total Faculty'], row['Average Fees']), axis=1)
    
    # Default sorting by rating in ascending order
    data = data.sort_values(by='Rating', ascending=True)
    
    # Create a frame for displaying the treeview and sorting options
    frame = tk.Frame(ratings_window)
    frame.pack(padx=10, pady=10, fill='both', expand=True)
    
    # Create a treeview to display the college data
    tree = ttk.Treeview(frame, columns=['College Name', 'Rating', 'Established Year', 'Average Fees'], show='headings')
    tree.heading('College Name', text='College Name')
    tree.heading('Rating', text='Rating')
    tree.heading('Established Year', text='Established Year')
    tree.heading('Average Fees', text='Average Fees')
    
    # Populate the treeview with data
    for index, row in data.iterrows():
        tree.insert('', 'end', values=(row['College Name'], row['Rating'], row['Established Year'], row['Average Fees']))
    
    tree.pack(fill='both', expand=True)
    
    # Add padding between the treeview and the dropdown menu
    padding = tk.Label(frame, text="", pady=10)
    padding.pack()
    
    # Function to handle sorting by rating
    def sort_by_rating(order):
        data_sorted = data.sort_values(by='Rating', ascending=(order == 'asc'))
        update_treeview(tree, data_sorted)
    
    # Create a StringVar to track the selected sorting option
    sort_option = tk.StringVar(ratings_window)
    
    # Function to handle selection in the dropdown menu
    def on_sort_option_change(*args):
        selected_option = sort_option.get()
        if selected_option != 'Sort By':
            if selected_option == 'High to Low':
                sort_by_rating('desc')
            elif selected_option == 'Low to High':
                sort_by_rating('asc')
    
    # Link the dropdown variable to the callback function
    sort_option.trace('w', on_sort_option_change)
    
    # Create the dropdown menu
    sort_options = ['Sort By', 'High to Low', 'Low to High']
    sort_option.set(sort_options[0])  # Set the default option to "Sort By"
    sort_menu = tk.OptionMenu(frame, sort_option, *sort_options)
    sort_menu.pack(pady=(0, 10))
    
    # Display the ratings window
    ratings_window.mainloop()

def update_treeview(tree, data):
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    # Populate the treeview with sorted data
    for index, row in data.iterrows():
        tree.insert('', 'end', values=(row['College Name'], row['Rating'], row['Established Year'], row['Average Fees']))
def display_college_ratings():
    # Read data from the CSV file
    data = pd.read_csv("datasets/colleges.csv")
    
    # Get unique college names
    college_names = data["College Name"].unique()
    
    # Create a new window to display college ratings
    ratings_window = tk.Toplevel(root)
    ratings_window.title("College Ratings")
    ratings_window.geometry("1100x900")
    center_window(ratings_window)
    
    # Create a treeview to display ratings
    tree = ttk.Treeview(ratings_window)
    tree["columns"] = ("Established Year", "Average Fees", "Rating")

    # Define column headings
    tree.heading("#0", text="College Name")
    tree.heading("Established Year", text="Established Year", anchor="center")  # Center the column
    tree.heading("Average Fees", text="Average Fees", anchor="center")  # Center the column
    tree.heading("Rating", text="Rating", anchor="center")  # Center the column

    # Insert data into the treeview
    for college in college_names:
        college_data = data[data["College Name"] == college].iloc[0]
        established_year = college_data["Established Year"]
        average_fees = college_data["Average Fees"]
        total_student_enrollments = college_data["Total Student Enrollments"]
        total_faculty = college_data["Total Faculty"]
        rating = calculate_rating(established_year=established_year, total_student_enrollments=total_student_enrollments, total_faculty=total_faculty, average_fees=average_fees)
        tree.insert("", "end", text=college, values=(established_year, average_fees, rating))

    # Pack the treeview
    tree.pack(expand=True, fill="both")

def display_ratings_window():
    # Read the college data from CSV
    try:
        colleges_df = pd.read_csv("datasets/colleges.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "Colleges dataset not found.")
        return

    # Create a new dataframe to store college ratings
    ratings_df = colleges_df.copy()

    # Calculate rating for each college
    ratings_df["Rating"] = ratings_df.apply(
        lambda row: calculate_rating(
            row["Established Year"],
            row["Total Student Enrollments"],
            row["Total Faculty"],
            row["Average Fees"],
        ),
        axis=1,
    )

    # Create a new window for displaying ratings
    ratings_window = tk.Toplevel()
    ratings_window.title("College Ratings")
    ratings_window.geometry("600x400")
    center_window(ratings_window)

    # Create a Treeview to display ratings
    tree = ttk.Treeview(ratings_window)
    tree["columns"] = ("Established Year", "Average Fees", "Rating")
    tree.heading("#0", text="College Name")
    tree.heading("Established Year", text="Established Year")
    tree.heading("Average Fees", text="Average Fees")
    tree.heading("Rating", text="Rating")

    # Center align the columns
    tree.column("#0", anchor=tk.CENTER)
    tree.column("Established Year", anchor=tk.CENTER)
    tree.column("Average Fees", anchor=tk.CENTER)
    tree.column("Rating", anchor=tk.CENTER)

    # Insert data into Treeview
    for index, row in ratings_df.iterrows():
        tree.insert("", index, text=row["College Name"], values=(
            row["Established Year"],
            row["Average Fees"],
            row["Rating"],
        ))

    tree.pack(expand=True, fill="both")

def exit_application():
    root.destroy()


def navigate_to_number_options():
    title_label.config(text="Welcome")
    label.config(
        text="Option 1 - View top x and bottom y rows.\nOption 2 - Export certain rows from dataset.\nOption 3 - Compare data between 2 colleges.\nOption 4 - View a brief info about a college.\nOption 5 - Display college ratings.",
    )
    enter_button.pack(side=tk.LEFT, padx=10)
    credits_button.pack(side=tk.LEFT, padx=10)
    exit_button.pack(side=tk.LEFT, padx=10)
    view_all_data.pack(side=tk.LEFT, padx=10)


# Initialize the logger
logger = logger()

# Connect to the MySQL database using the provided configuration
# mydb = msc.connect(
#     host=config.host,
#     user=config.user,
#     password=config.password,
# )

# Log information: Sending initial connection to the database, awaiting response.
logger.log("INFO", "Sending initial connection to the database, awaiting response.")

try:
    if True:
        # Open tkinter box after database operations are completed
        root = tk.Tk()
        root.title(config.projectName)
        root.geometry("700x500")
        center_window(root)
        root.config(bg=config.accentColor)

        title_label = tk.Label(
            root,
            text="Welcome",
            fg=config.fontColor,
            bg=config.accentColor,
            font=("Montserrat", 16, "bold"),
        )
        title_label.pack(pady=20)

        label = tk.Label(
            root,
            text="Select a button to get started.",
            fg=config.fontColor,
            bg=config.accentColor,
            font=("Montserrat", 12),
        )
        label.pack(pady=10)

        button_frame = tk.Frame(root, bg=config.accentColor)
        button_frame.pack(pady=10)

        enter_button = Button(
            button_frame,
            text="Enter",
            command=on_enter_button_click,
            style="Montserrat.TButton",
        )
        enter_button.pack(side=tk.LEFT, padx=10)

        exit_button = Button(
            button_frame, text="Exit", command=on_exit, style="Montserrat.TButton"
        )
        exit_button.pack(side=tk.RIGHT, padx=10)

        credits_button = Button(
            button_frame,
            text="Credits",
            command=show_credits,
            style="Montserrat.TButton",
        )
        credits_button.pack(
            side=tk.LEFT, padx=10
        )  # Change this to left to align with other buttons

        go_back_button = Button(
            button_frame,
            text="Go back to main menu",
            command=go_back_to_main_menu,
            style="Montserrat.TButton",
        )
        go_back_button.pack_forget()

        view_all_data = Button(
            button_frame,
            text="View all data",
            command=show_csv_data,
            style="Montserrat.TButton",
        )
        view_all_data.pack(side=tk.LEFT, padx=10)
        option1 = Button(
            button_frame, text="1", command=show_head_tail, style="Montserrat.TButton"
        )
        option1.pack_forget()
        option2 = Button(
            button_frame, text="2", command=export_csv_data, style="Montserrat.TButton"
        )
        option2.pack_forget()
        option3 = Button(
            button_frame,
            text="3",
            command=lambda: compare_colleges_window(),
            style="Montserrat.TButton",
        )
        option3.pack_forget()
        option4 = ttk.Button(
            button_frame,
            text="4",
            command=search_college,
            style="Montserrat.TButton",
        )
        option4.pack_forget()
        option5 = ttk.Button(
            button_frame,
            text="5",
            command=open_college_ratings_window,
            style="Montserrat.TButton",
        )
        option5.pack_forget()
        return_to_main_menu = Button(
            button_frame,
            text="Return to main menu",
            command=go_back_to_main_menu,
            style="Montserrat.TButton",
        )
        # Define a custom style for the buttons to use Montserrat font
        style = tk.ttk.Style()
        style.configure("Montserrat.TButton", font=("Montserrat", 12))

        root.mainloop()

        # Log success information: Database connected successfully. Use the CLI or GUI to start querying.
        logger.log(
            "SUCCESS",
            "Database connected successfully, use the CLI or GUI to start querying.",
        )

except Exception as e:
    # Log error: State the error name and print the error stack
    logger.log(
        "ERROR", "Client request was sent, but the server rejected the handshake."
    )
    logger.log("ERROR", f"An error occurred: {e}")
