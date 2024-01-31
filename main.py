import mysql.connector as msc
import numpy as np
import connectors.config as config
from src.utils import CustomLogger as logger
from connectors.init import Initialize
from connectors.insert import Insert
from connectors.config import connection
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Button, Combobox
import threading
from tkinter.simpledialog import askinteger
import pandas as pd
from tkinter import StringVar
from tkinter import ttk, font
import matplotlib.pyplot as plt
from tkinter import filedialog

animation_running = True


def center_window(window):
    """
    Centers the given window on the screen.

    Args:
        window: The window to be centered.

    Returns:
        None
    """
    window.update_idletasks()  # Make sure window size is updated
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def show_credits():
    """
    Function to display credits with team lead and contributors.
    No parameters.
    No return types.
    """
    title_label.config(text="Credits", font=("Montserrat", 16, "bold"))
    label.config(
        text=""" Shree Nandha A B                  -   Team Lead
      Janardan M                              -   Contributor #1
      Naveen Sabari Rajhan R S    -   Contributor #2""",
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
    """
    Function to go back to the main menu and reset the window layout.
    """
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
    """
    Function to display the head and tail of a dataset and update the display based on column selection.
    """
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
            """
            Update the display with the selected column data.

            This function does not take any parameters and does not return any value.
            """
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


def on_enter_button_click():
    """
    This function handles the click event for the "Enter" button. It centers the window,
    starts an animation thread, and initiates the database initialization and data insertion
    processes in separate threads. It also removes the "Credits" button when the "Enter"
    button is clicked.
    """
    center_window(root)

    def update_text_animation(dot_count):
        """
        Update the text animation on the label based on the dot_count.
        If animation_running is True, it updates the label text and disables the buttons.
        If animation_running is False, it enables the buttons.
        """
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
        """
        Finish inserting data and update the UI accordingly.
        """
        global animation_running
        animation_running = False
        '''initialize_and_insert_data'''
        '''cursor = connection.cursor()
        Insert.db(connection)
        Insert.from_csv(connection, 'D:/nand3v/datasets/colleges.csv')'''
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
        """
        Function to initialize the database and insert data from a CSV file.
        """
        Insert.db(connection)
        Insert.from_csv(connection, "./datasets/colleges.csv")
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
    """
    Function to display CSV data in a GUI window.

    This function sets up a GUI window to display data from a CSV file. It
    includes functions to load data for each page, show a specific page, and
    set up the Treeview widget to display the data. It also includes buttons
    for navigating between pages of data.

    No parameters or return types are explicitly mentioned in the function
    definition, but the function relies on external variables and libraries
    such as 'root', 'pd', and 'tk'.
    """
    center_window(root)
    csv_file_path = "datasets/colleges.csv"  # Update with your actual CSV file path
    page_size = 50  # Number of rows per page

    def load_data(page_num):
        """
        Load data from a CSV file based on the given page number.

        Args:
            page_num (int): The page number to load.

        Returns:
            pandas.DataFrame: The data for the specified page.
        """
        center_window(root)
        start_idx = page_num * page_size
        end_idx = start_idx + page_size

        data = pd.read_csv(csv_file_path)
        page_data = data.iloc[start_idx:end_idx]

        return page_data

    def show_page(page_num):
        """
        Show the specified page by updating the current_page variable and loading data into the Treeview.

        Parameters:
        page_num (int): The page number to be shown.

        Returns:
        None
        """
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
    """
    Perform a search and comparison operation.

    This function takes no parameters and does not return any value.
    It retrieves the search query from the search entry field, removes any leading
    or trailing whitespace, and then searches for the most related college name in
    the 'data' DataFrame. If a related college name is found, it retrieves the
    college name and compares it with the selected college using the
    'compare_colleges' function. If no search query is provided, it displays a
    message box with an error message.
    """
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
    """
    Compare two colleges based on various data points and display the comparison through bar graphs.

    Args:
    college1: A string representing the name of the first college.
    college2: A string representing the name of the second college.

    Returns:
    None
    """
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
    """
    Parse the campus size from the given value.

    Args:
        value (str): The input value to parse.

    Returns:
        float: The parsed campus size, or 0.0 if the value is not in the expected format.
    """
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
    """
    This function is responsible for exporting CSV data. It includes nested functions to
    load data, show a page, navigate to the previous or next page, and save changes to
    the data. The function initializes a GUI window for editing CSV data and interacting
    with the data through a Treeview widget. It also includes functionality for saving
    the data with a custom file extension and displaying the data in a specific format.
    """
    global data  # Make sure data is a global variable accessible in this function
    data = pd.read_csv(
        "./datasets/colleges.csv",
    )

    def load_data(page_num):
        """
        Load data from the specified page number.

        :param page_num: The page number to load data from
        :return: The data loaded from the specified page number
        """
        start_idx = page_num * page_size
        end_idx = start_idx + page_size

        return data.iloc[start_idx:end_idx]

    def show_page(page_num):
        """
        Updates the current page number and refreshes the Treeview with new page data.

        :param page_num: int - The page number to display
        :return: None
        """
        nonlocal current_page  # Use nonlocal to update the outer current_page variable
        current_page = page_num

        tree.delete(*tree.get_children())  # Clear existing data in the Treeview
        page_data = load_data(page_num)

        for index, row in page_data.iterrows():
            tree.insert("", "end", values=row.tolist())

    def prev_page():
        """
        Function to go to the previous page if the current page is greater than 0.
        No parameters and no return value.
        """
        if current_page > 0:
            show_page(current_page - 1)

    def next_page():
        """
        This function calculates the last page based on the length of the data and the page size.
        If the current page is less than the last page, it shows the next page.
        """
        last_page = (len(data) - 1) // page_size
        if current_page < last_page:
            show_page(current_page + 1)

    def save_changes():
        """
        Save the changes made in the treeview to a file with user-selected file extension.
        """
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
            """
            Saves the updated data to a file with the specified extension.

            This function prompts the user to select a file location to save the updated data
            based on the chosen file extension. If the user selects a valid location, it saves
            the updated data to the specified file in the chosen format. If the user selects an
            invalid extension, an error message is displayed. The function does not return
            anything.

            Parameters:
            - None

            Returns:
            - None
            """
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
        """
        A function to finish editing a tree item with the new value from the entry.

        :param event: The event triggering the editing finish.
        :param item: The item in the tree being edited.
        :param row: The row of the item in the tree.
        :param col: The column of the item being edited.
        :return: None
        """
        new_value = entry_var.get()
        tree.item(item, values=("", new_value, ""))
        entry.place_forget()
        entry.unbind("<FocusOut>")

    def save_changes():
        """
        Function to save the changes made in the treeview to a file with the user-selected file extension.
        """
        updated_data = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            updated_data.append(values)

        # Convert the updated data back to a DataFrame
        updated_df = pd.DataFrame(updated_data, columns=data.columns)

        # Define supported file extensions
        supported_extensions = ["csv", "xlsx", "json", "html"]

        def save_with_extension():
            """
            Saves the updated data to a file with the specified user_extension.
            Prompts the user to select a file location and saves the updated data in the
            specified format (csv, xlsx, json, or html). Shows an error message if the
            user selects an unsupported file extension, and shows a success message after
            saving the file. Also hides the extension_button after the save operation.
            """
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
            """
            Opens a new window to select a file extension using a Combobox and a save button.
            """
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
        """
        This function compares two colleges based on the values of college1_var and college2_var.
        """
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
    """
    Function to search for a college in the dataset based on a case-insensitive search for college names.
    """
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


def display_results_window(result):
    """
    Display the search results in a new window.

    Args:
        result (dict): A dictionary containing the search results for a college.

    Returns:
        None
    """
    results_window = tk.Toplevel()
    results_window.title("Search Results")
    results_window.geometry("1100x900")
    center_window(results_window)
    text_widget = tk.Text(results_window, font=("Montserrat", 14))
    text_widget.pack(fill="both", expand=True)

    text_widget.tag_configure("bold", font=("Montserrat", 18, "bold"))

    text_widget.insert("end", f"College Name: {result['College Name']}\n", "bold")
    text_widget.insert("end", f"Genders Accepted: {result['Genders Accepted']}\n")
    text_widget.insert("end", f"Campus Size: {result['Campus Size']}\n")
    text_widget.insert(
        "end", f"Total Student Enrollments: {result['Total Student Enrollments']}\n"
    )
    text_widget.insert("end", f"Total Faculty: {result['Total Faculty']}\n")
    text_widget.insert("end", f"Established Year: {result['Established Year']}\n")
    text_widget.insert("end", f"Rating: {result['Rating']}\n")
    text_widget.insert("end", f"University: {result['University']}\n")
    text_widget.insert("end", f"City: {result['City']}\n")
    text_widget.insert("end", f"State: {result['State']}\n")
    text_widget.insert("end", f"Country: {result['Country']}\n")
    text_widget.insert("end", f"Average Fees: {result['Average Fees']}\n")
    # Append courses with "-"
    courses = result["Courses"].split(",")
    formatted_courses = "\n".join([f"- {course.strip()}" for course in courses])
    text_widget.insert("end", f"Courses: ...\n{formatted_courses}\n")

    text_widget.insert("end", f"Facilities: {result['Facilities']}\n")
    text_widget.insert("end", f"College Type: {result['College Type']}\n")
    text_widget.configure(state="disabled")


def calculate_rating(
    established_year, total_student_enrollments, total_faculty, average_fees
):
    """
    Calculate the rating of a college based on various factors such as established year,
    total student enrollments, total faculty, and average fees. Parameters:
    - established_year: the year the college was established
    - total_student_enrollments: the total number of students enrolled in the college
    - total_faculty: the total number of faculty in the college
    - average_fees: the average fees of the college
    Returns a string representing the calculated rating in the format 'x.xx/5'
    """
    # Convert established_year to integer if it's not NaN and not 'Established Year'
    if established_year != "Established Year" and not pd.isnull(established_year):
        established_year = int(established_year)
    else:
        established_year = 0

    # Convert other values to integers or floats if they are not NaN
    try:
        total_faculty = int(total_faculty) if not pd.isnull(total_faculty) else 0
        total_student_enrollments = (
            int(total_student_enrollments)
            if not pd.isnull(total_student_enrollments)
            else 0
        )
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
            (adjusted_established_year * established_year_weight)
            + (
                (total_faculty / total_student_enrollments)
                * student_faculty_ratio_weight
            )
            + ((1 / average_fees) * average_fees_weight)
            + (
                campus_size_weight / np.sqrt(total_student_enrollments)
            )  # Adjust for campus size
        )
    except ZeroDivisionError:
        rating = 0  # Handle division by zero

    # Scale rating between 0 and 5
    scaled_rating = min(max(rating / 5, 0), 5)

    return f"{scaled_rating:.2f}/5"


def open_college_ratings_window():
    """
    Create a new window for displaying college ratings
    """
    ratings_window = tk.Toplevel(root)
    ratings_window.title("College Ratings")

    # Create a DataFrame to hold the data
    data = pd.read_csv("./datasets/colleges.csv")

    # Calculate ratings for each college
    data["Rating"] = data.apply(
        lambda row: calculate_rating(
            row["Established Year"],
            row["Total Student Enrollments"],
            row["Total Faculty"],
            row["Average Fees"],
        ),
        axis=1,
    )

    # Default sorting by rating in ascending order
    data = data.sort_values(by="Rating", ascending=False)

    # Create a frame for displaying the treeview and sorting options
    frame = tk.Frame(ratings_window)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Create a treeview to display the college data
    tree = ttk.Treeview(
        frame,
        columns=["College Name", "Rating", "Established Year", "Average Fees"],
        show="headings",
    )
    tree.heading("College Name", text="College Name")
    tree.heading("Rating", text="Rating")
    tree.heading("Established Year", text="Established Year")
    tree.heading("Average Fees", text="Average Fees")

    # Populate the treeview with data
    for index, row in data.iterrows():
        tree.insert(
            "",
            "end",
            values=(
                row["College Name"],
                row["Rating"],
                row["Established Year"],
                row["Average Fees"],
            ),
        )

    tree.pack(fill="both", expand=True)

    # Add padding between the treeview and the dropdown menu
    padding = tk.Label(frame, text="", pady=10)
    padding.pack()

    # Function to handle sorting by rating
    def sort_by_rating(order):
        """
        Sorts the data by rating in either ascending or descending order.

        Parameters:
            order (str): The order in which to sort the data, either 'asc' for ascending or 'desc' for descending.

        Returns:
            None
        """
        data_sorted = data.sort_values(by="Rating", ascending=(order == "asc"))
        update_treeview(tree, data_sorted)

    # Create a StringVar to track the selected sorting option
    sort_option = tk.StringVar(ratings_window)

    # Function to handle selection in the dropdown menu
    def on_sort_option_change(*args):
        """
        This function handles the change event for the sort option. It takes in
        *args as parameters and does not return any value.
        """
        selected_option = sort_option.get()
        if selected_option != "Sort By":
            if selected_option == "High to Low":
                sort_by_rating("desc")
            elif selected_option == "Low to High":
                sort_by_rating("asc")

    # Link the dropdown variable to the callback function
    sort_option.trace("w", on_sort_option_change)

    # Create the dropdown menu
    sort_options = ["Sort By", "High to Low", "Low to High"]
    sort_option.set(sort_options[0])  # Set the default option to "Sort By"
    sort_menu = tk.OptionMenu(frame, sort_option, *sort_options)
    sort_menu.pack(pady=(0, 10))

    # Display the ratings window
    ratings_window.mainloop()


def update_treeview(tree, data):
    """
    Update the given treeview with the provided data.

    Args:
        tree: The treeview to be updated.
        data: The data to populate the treeview with.

    Returns:
        None
    """
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)

    # Populate the treeview with sorted data
    for index, row in data.iterrows():
        tree.insert(
            "",
            "end",
            values=(
                row["College Name"],
                row["Rating"],
                row["Established Year"],
                row["Average Fees"],
            ),
        )


def display_college_ratings():
    """
    Display college ratings by reading data from a CSV file and creating a new window to show the ratings using a treeview.
    """
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
    tree.heading(
        "Established Year", text="Established Year", anchor="center"
    )  # Center the column
    tree.heading(
        "Average Fees", text="Average Fees", anchor="center"
    )  # Center the column
    tree.heading("Rating", text="Rating", anchor="center")  # Center the column

    # Insert data into the treeview
    for college in college_names:
        college_data = data[data["College Name"] == college].iloc[0]
        established_year = college_data["Established Year"]
        average_fees = college_data["Average Fees"]
        total_student_enrollments = college_data["Total Student Enrollments"]
        total_faculty = college_data["Total Faculty"]
        rating = calculate_rating(
            established_year=established_year,
            total_student_enrollments=total_student_enrollments,
            total_faculty=total_faculty,
            average_fees=average_fees,
        )
        tree.insert(
            "", "end", text=college, values=(established_year, average_fees, rating)
        )

    # Pack the treeview
    tree.pack(expand=True, fill="both")


def display_ratings_window():
    """
    Display a ratings window for colleges based on data from a CSV file.
    Read the college data from CSV, calculate ratings for each college, and
    display the ratings in a new window using Treeview.
    """
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
        tree.insert(
            "",
            index,
            text=row["College Name"],
            values=(
                row["Established Year"],
                row["Average Fees"],
                row["Rating"],
            ),
        )

    tree.pack(expand=True, fill="both")


def exit_application():
    """
    Close the application window and drop the database before exit.
    """
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE db;")
    cursor.execue("COMMIT;")
    root.destroy()


def navigate_to_number_options():
    """
    Navigates to the number options and configures the title label and label text.
    Packs the enter button, credits button, exit button, and view all data button.
    """
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
        root.geometry("1100x800")
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
            button_frame, text="Exit", command=exit_application, style="Montserrat.TButton"
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
