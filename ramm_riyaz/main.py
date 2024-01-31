import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
from tkinter import ttk

# Load the data
data = pd.read_csv("./dataset.csv")
#C:\Users\MACH-001\Desktop\Modal Pratical\Project
# Create the main GUI window
root = tk.Tk()
root.title("Startup Data Analysis")
root.geometry("800x600")


# Center root windows by calling it upon a root object
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2
    window.geometry(f"+{x_offset}+{y_offset}")


# Function to display startup information
def display_info():
    selected_option = option_var.get()

    if selected_option == 1:
        # Display Specific Columns
        columns_frame = tk.Toplevel(root)
        columns_frame.title("Display Specific Columns")

        def show_columns():
            selected_columns = columns_listbox.curselection()
            for item in result_tree.get_children():
                result_tree.delete(item)  # Clear existing data in Treeview
            for idx in selected_columns:
                col_name = columns_listbox.get(idx)
                for value in data[col_name]:
                    result_tree.insert("", "end", values=(col_name, value))

        columns_listbox = tk.Listbox(columns_frame, selectmode=tk.SINGLE)
        columns_listbox.pack(padx=20, pady=20)

        for col in data.columns:
            columns_listbox.insert(tk.END, col)

        show_button = tk.Button(
            columns_frame, text="Show Selected Columns", command=show_columns
        )
        show_button.pack(pady=10)

        result_tree = ttk.Treeview(
            columns_frame, columns=("column1", "column2"), show="headings", height=35
        )
        result_tree.column("#1", width=700)
        result_tree.column("#2", width=700)

        result_tree.heading("#1", text="Column")
        result_tree.heading("#2", text="Value")
        result_tree.pack(padx=20, pady=20)
        center_window(columns_frame)

    elif selected_option == 2:
        # Sort Startups by Year
        sort_frame = tk.Toplevel(root)
        sort_frame.title("Sort Startups by Year")

        def sort_startups():
            selected_sort = sort_var.get()
            ascending = True if selected_sort == "A" else False
            sorted_data = data.sort_values(by="Year", ascending=ascending)

            result_text.delete("1.0", tk.END)  # Clear previous content

            if not sorted_data.empty:
                for idx, row in sorted_data.iterrows():
                    result_text.insert(tk.END, f"Row {idx+1}:\n")
                    result_text.insert(
                        tk.END, f"Incubation Center: {row['Incubation_Center']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Startup Name: {row['Name_of_the_startup']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Location of Company: {row['Location_of_company']}\n"
                    )
                    result_text.insert(tk.END, f"Sector: {row['Sector']}\n")
                    result_text.insert(
                        tk.END, f"Company Profile: {row['Company_profile']}\n"
                    )
                    result_text.insert(tk.END, f"Starting Year: {row['Year']}\n")
                    result_text.insert(
                        tk.END, f"Corporate Identification Number: {row['CIN']}\n"
                    )
                                        
                    result_text.insert(
                        tk.END, f"Paid-up Capital: {row['Paid_up_capital']}\n"
                    )
                
                    result_text.insert(tk.END, "\n")
            else:
                result_text.insert(tk.END, "No startups found.\n")

        sort_label = tk.Label(sort_frame, text="Sort in ascending or descending order:")
        sort_label.pack(padx=20, pady=10)

        sort_var = tk.StringVar(value="A")
        sort_radio_asc = tk.Radiobutton(
            sort_frame, text="Ascending", variable=sort_var, value="A"
        )
        sort_radio_desc = tk.Radiobutton(
            sort_frame, text="Descending", variable=sort_var, value="D"
        )
        sort_radio_asc.pack()
        sort_radio_desc.pack()

        sort_button = tk.Button(sort_frame, text="Sort Startups", command=sort_startups)
        sort_button.pack(pady=10)

        result_text = tk.Text(
            sort_frame,
            wrap=tk.WORD,
            height=15,
            width=70,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)
        center_window(sort_frame)

    elif selected_option == 3:
        # Display All Starting Years of the Startup
        years_frame = tk.Toplevel(root)
        years_frame.title("Display All Starting Years of the Startup")

        years = data["Year"].unique()

        result_text = tk.Text(
            years_frame,
            wrap=tk.WORD,
            height=15,
            width=70,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)
        result_text.insert(tk.END, "All Starting Years of the Startup:\n")
        result_text.insert(tk.END, ", ".join(map(str, years)) + "\n\n")
        center_window(years_frame)

    elif selected_option == 4:
        # Display All Startup Names
        names_frame = tk.Toplevel(root)
        names_frame.title("Display All Startup Names")

        startup_names = data["Name_of_the_startup"].unique()

        result_text = tk.Text(
            names_frame,
            wrap=tk.WORD,
            height=15,
            width=70,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)
        result_text.insert(tk.END, "All Startup Names:\n")
        result_text.insert(tk.END, "\n".join(startup_names) + "\n\n")
        center_window(names_frame)

    elif selected_option == 5:
        startup_name_frame = tk.Toplevel(root)
        startup_name_frame.title("Know About the Incubation Center of the Startup")

        startup_name_var = tk.StringVar()
        startup_name_label = tk.Label(startup_name_frame, text="Enter Startup Name:")
        startup_name_label.pack(padx=20, pady=10)

        startup_name_entry = tk.Entry(startup_name_frame, textvariable=startup_name_var)
        startup_name_entry.pack(padx=20, pady=10)

        location_text = tk.Text(
            startup_name_frame,
            wrap=tk.WORD,
            height=3,
            width=40,
            state="normal",
            font=("Arial", 14),
        )
        location_text.pack(padx=20, pady=10)

        def display_location():
            startup_name = startup_name_var.get()
            startup_data = data[
                data["Name_of_the_startup"]
                .str.lower()
                .str.contains(startup_name.lower())
            ]
            if not startup_data.empty:
                location = startup_data["Location_of_company"].values[0]
                location_text.delete(1.0, tk.END)  # Clear previous content
                location_text.insert(tk.END, location)
            else:
                location_text.delete(1.0, tk.END)
                location_text.insert(tk.END, "Startup not found!")

        display_button = tk.Button(
            startup_name_frame, text="Display Incubation Center", command=display_location
        )
        display_button.pack(pady=10)
        center_window(root)

        

    elif selected_option == 6:
        # Know About the Location of the Startup
        location_frame = tk.Toplevel(root)
        location_frame.title("Know About the Location of the Startup")

        def display_location():
            startup_name = startup_name_var.get()
            startup_data = data[
                data["Name_of_the_startup"]
                .str.lower()
                .str.contains(startup_name.lower())
            ]
            if not startup_data.empty:
                location = startup_data["Location_of_company"].values[0]
                if len(location) > 0:
                    result_label.config(text=f"The Location of {startup_name} is in {startup_data['Location_of_company'].values[0]}")
                else:
                    result_label.config(text="Location data not available")
            else:
                result_label.config(text="Startup not found!")


        startup_name_var = tk.StringVar()
        startup_name_label = tk.Label(location_frame, text="Enter Startup Name:")
        startup_name_label.pack(padx=20, pady=10)
        startup_name_entry = tk.Entry(location_frame, textvariable=startup_name_var)
        startup_name_entry.pack(padx=20, pady=10)
        display_button = tk.Button(
            location_frame, text="Display Location", command=display_location
        )
        display_button.pack(pady=10)
        result_label = tk.Label(location_frame, text="")
        result_label.pack(padx=20, pady=20)
        center_window(location_frame)

    elif selected_option == 7:
        # Know About the Type of Sector of the Startup
        sector_frame = tk.Toplevel(root)
        sector_frame.title("Know About the Type of Sector of the Startup")

        def display_sector():
            startup_name = startup_name_var.get()
            startup_data = data[
                data["Name_of_the_startup"]
                .str.lower()
                .str.contains(startup_name.lower())
            ]
            if not startup_data.empty:
                sector = startup_data["Sector"].values[0]
                result_label.config(text=f"The Sector of {startup_name} is {sector}")
            else:
                result_label.config(text="Startup not found!")

        startup_name_var = tk.StringVar()
        startup_name_label = tk.Label(sector_frame, text="Enter Startup Name:")
        startup_name_label.pack(padx=20, pady=10)
        startup_name_entry = tk.Entry(sector_frame, textvariable=startup_name_var)
        startup_name_entry.pack(padx=20, pady=10)
        display_button = tk.Button(
            sector_frame, text="Display Sector", command=display_sector
        )
        display_button.pack(pady=10)
        result_label = tk.Label(sector_frame, text="")
        result_label.pack(padx=20, pady=20)
        center_window(sector_frame)

    elif selected_option == 8:
        # Know the Profile of the Startup
        profile_frame = tk.Toplevel(root)
        profile_frame.title("Know the Profile of the Startup")

        def display_profile():
            startup_name = startup_name_var.get()
            profile = data[data["Name_of_the_startup"]
                .str.lower()
                .str.contains(startup_name.lower())
            ][
                "Company_profile"
            ].values[0]
            result_label.config(text=f"The Profile of {startup_name} is {profile}")

        startup_name_var = tk.StringVar()
        startup_name_label = tk.Label(profile_frame, text="Enter Startup Name:")
        startup_name_label.pack(padx=20, pady=10)
        startup_name_entry = tk.Entry(profile_frame, textvariable=startup_name_var)
        startup_name_entry.pack(padx=20, pady=10)
        display_button = tk.Button(
            profile_frame, text="Display Profile", command=display_profile
        )
        display_button.pack(pady=10)
        result_label = tk.Label(
            profile_frame, 
            text="", 
            width=60,  # Adjust width as needed
            wraplength=500,  # Adjust wrap length as needed
            anchor="center"  # Center align the text
        )
        result_label.pack(padx=20, pady=20)
        result_label.pack(padx=20, pady=20)
        center_window(profile_frame)

    elif selected_option == 9:
        # Know the Corporate Identification Number of the Startup
        cin_frame = tk.Toplevel(root)
        cin_frame.title("Know the Corporate Identification Number of the Startup")

        def display_cin():
            startup_name = startup_name_var.get()
            cin = data[data["Name_of_the_startup"]
                .str.lower()
                .str.contains(startup_name.lower())
            ]["CIN"].values[0]
            result_label.config(
                text=f"The Corporate Identification Number of {startup_name} is {cin}"
            )

        startup_name_var = tk.StringVar()
        startup_name_label = tk.Label(cin_frame, text="Enter Startup Name:")
        startup_name_label.pack(padx=20, pady=10)
        startup_name_entry = tk.Entry(cin_frame, textvariable=startup_name_var)
        startup_name_entry.pack(padx=20, pady=10)
        display_button = tk.Button(cin_frame, text="Display CIN", command=display_cin)
        display_button.pack(pady=10)
        result_label = tk.Label(cin_frame, text="")
        result_label.pack(padx=20, pady=20)
        center_window(cin_frame)

    elif selected_option == 10:
        # Know the Paid-up Capital of the Startup
        capital_frame = tk.Toplevel(root)
        capital_frame.title("Know the Paid-up Capital of the Startup")

        def display_paid_up_capital():
            startup_name = startup_name_var.get()
            capital = data[data["Name_of_the_startup"]
                .str.lower()
                .str.contains(startup_name.lower())
            ][
                "Paid_up_capital"
            ].values[0]
            result_label.config(
                text=f"The Paid-up Capital of {startup_name} is {capital}"
            )

        startup_name_var = tk.StringVar()
        startup_name_label = tk.Label(capital_frame, text="Enter Startup Name:")
        startup_name_label.pack(padx=20, pady=10)
        startup_name_entry = tk.Entry(capital_frame, textvariable=startup_name_var)
        startup_name_entry.pack(padx=20, pady=10)
        display_button = tk.Button(
            capital_frame,
            text="Display Paid-up Capital",
            command=display_paid_up_capital,
        )
        display_button.pack(pady=10)
        result_label = tk.Label(capital_frame, text="")
        result_label.pack(padx=20, pady=20)
        center_window(capital_frame)

    elif selected_option == 11:
        # Filter the Startups Using Locations
        location_filter_frame = tk.Toplevel(root)
        location_filter_frame.title("Filter the Startups Using Locations")

        # Preprocess Location_of_company column
        cleaned_locations = [
            location.strip("', []") for location in data["Location_of_company"].unique()
        ]

        def filter_by_location():
            selected_location = location_var.get()
            filtered_data = data[data["Location_of_company"]
                .str.lower()
                .str.contains(selected_location.lower())
            ]
            result_text.delete("1.0", tk.END)  # Clear previous content

            if not filtered_data.empty:
                for idx, row in filtered_data.iterrows():
                    result_text.insert(tk.END, f"Row {idx+1}:\n")
                    result_text.insert(
                        tk.END, f"Incubation Center: {row['Incubation_Center']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Startup Name: {row['Name_of_the_startup']}\n"
                    )

                    # Clean up Location_of_company value
                    cleaned_location = row["Location_of_company"].strip("', []")
                    result_text.insert(
                        tk.END, f"Location of Company: {cleaned_location}\n"
                    )

                    result_text.insert(tk.END, f"Sector: {row['Sector']}\n")
                    result_text.insert(
                        tk.END, f"Company Profile: {row['Company_profile']}\n"
                    )
                    result_text.insert(tk.END, f"Starting Year: {row['Year']}\n")
                    result_text.insert(
                        tk.END, f"Corporate Identification Number: {row['CIN']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Paid-up Capital: {row['Paid_up_capital']}\n"
                    )
                    result_text.insert(tk.END, "\n")
            else:
                result_text.insert(tk.END, "No startups found.\n")

        location_var = tk.StringVar()
        location_label = tk.Label(location_filter_frame, text="Select Location:")
        location_label.pack(padx=20, pady=10)

        location_combobox = ttk.Combobox(
            location_filter_frame, textvariable=location_var, values=cleaned_locations
        )
        location_combobox.pack(padx=20, pady=10)

        display_button = tk.Button(
            location_filter_frame, text="Filter", command=filter_by_location
        )
        display_button.pack(pady=10)

        result_text = tk.Text(
            location_filter_frame,
            wrap=tk.WORD,
            height=15,
            width=70,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)
        center_window(location_filter_frame)

    elif selected_option == 12:
        # Filter the Startups Using Incubation Center
        incubation_filter_frame = tk.Toplevel(root)
        incubation_filter_frame.title("Filter the Startups Using Incubation Center")
        cleaned_incubation_centers = [
            center.strip("', []") for center in data["Incubation_Center"].unique()
        ]

        def filter_by_incubation():
            selected_incubation = incubation_var.get()
            filtered_data = data[data["Incubation_Center"] == selected_incubation]
            result_text.delete("1.0", tk.END)  # Clear previous content

            if not filtered_data.empty:
                for idx, row in filtered_data.iterrows():
                    result_text.insert(tk.END, f"Row {idx+1}:\n")
                    result_text.insert(
                        tk.END, f"Incubation Center: {row['Incubation_Center']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Startup Name: {row['Name_of_the_startup']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Location of Company: {row['Location_of_company']}\n"
                    )
                    result_text.insert(tk.END, f"Sector: {row['Sector']}\n")
                    result_text.insert(
                        tk.END, f"Company Profile: {row['Company_profile']}\n"
                    )
                    result_text.insert(tk.END, f"Starting Year: {row['Year']}\n")
                    result_text.insert(
                        tk.END, f"Corporate Identification Number: {row['CIN']}\n"
                    )
                    result_text.insert(
                        tk.END, f"Paid-up Capital: {row['Paid_up_capital']}\n"
                    )
                    result_text.insert(tk.END, "\n")
            else:
                result_text.insert(tk.END, "No startups found.\n")

        incubation_var = tk.StringVar()
        incubation_label = tk.Label(
            incubation_filter_frame, text="Select Incubation Center:"
        )
        incubation_label.pack(padx=20, pady=10)

        incubation_combobox = ttk.Combobox(
            incubation_filter_frame,
            textvariable=incubation_var,
            values=cleaned_incubation_centers,
        )
        incubation_combobox.pack(padx=20, pady=10)

        display_button = tk.Button(
            incubation_filter_frame, text="Filter", command=filter_by_incubation
        )
        display_button.pack(pady=10)

        result_text = tk.Text(
            incubation_filter_frame,
            wrap=tk.WORD,
            height=20,
            width=100,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)
        center_window(incubation_filter_frame)

    elif selected_option == 13:
        # Filter the Startups Using Starting Year
        year_filter_frame = tk.Toplevel(root)
        year_filter_frame.title("Filter the Startups Using Starting Year")

        def filter_by_year():
            # Clear previous items
            result_tree.delete(*result_tree.get_children())

            selected_year = int(year_var.get())
            filtered_data = data[data["Year"] == selected_year]

            # Define display names for columns
            display_names = {
                "Incubation_Center": "Incubation Centre",
                "Name_of_the_startup": "Startup Name",
                "Location_of_company": "Location of Company",
                "Sector": "Sector",
                "Company_profile": "Company Profile",
                "Year": "Starting Year",
                "CIN": "CIN",
                "Paid_up_capital": "Paid-up Capital",
            }

            if not filtered_data.empty:
                for idx, row in filtered_data.iterrows():
                    for column, value in row.items():
                        display_name = display_names.get(column, column)
                        result_tree.insert("", "end", values=(display_name, value))
            else:
                result_tree.insert("", "end", values=("No startups found.", ""))

        year_var = tk.StringVar()
        year_label = tk.Label(year_filter_frame, text="Enter Starting Year:")
        year_label.pack(padx=20, pady=10)

        year_entry = tk.Entry(year_filter_frame, textvariable=year_var)
        year_entry.pack(padx=20, pady=10)

        display_button = tk.Button(
            year_filter_frame, text="Filter", command=filter_by_year
        )
        display_button.pack(pady=10)

        result_tree = ttk.Treeview(
            year_filter_frame,
            columns=("column1", "column2"),
            show="headings",
            height=35,
        )
        result_tree.column("#1", width=150)  # Width of the first column (Column)
        result_tree.column("#2", width=700)  # Width of the second column (Value)

        result_tree.heading("#1", text="Columns")
        result_tree.heading("#2", text="Values")
        result_tree.pack(padx=20, pady=20)
        center_window(year_filter_frame)

    elif selected_option == 14:
        capital_frame = tk.Toplevel(root)
        capital_frame.title("Display the Rows with Paid-up Capital (Min|Max)")

        min_max_label = tk.Label(capital_frame, text="Select Min/Max:")
        min_max_label.pack(padx=20, pady=10)

        min_max_var = tk.StringVar(value="Min")
        min_radio = tk.Radiobutton(
            capital_frame, text="Minimum", variable=min_max_var, value="Min"
        )
        max_radio = tk.Radiobutton(
            capital_frame, text="Maximum", variable=min_max_var, value="Max"
        )
        min_radio.pack()
        max_radio.pack()

        result_text = tk.Text(
            capital_frame,
            wrap=tk.WORD,
            height=40,
            width=200,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)

        def display_min_max():
            selected_min_max = min_max_var.get()
            if selected_min_max == "Min":
                startup = data[data["Paid_up_capital"] == data["Paid_up_capital"].min()]
            else:
                startup = data[data["Paid_up_capital"] == data["Paid_up_capital"].max()]

            result_text.delete("1.0", tk.END)  # Clear previous content

            # Define display names for columns
            display_names = {
                "Incubation_Center": "Incubation Centre",
                "Name_of_the_startup": "Startup Name",
                "Location_of_company": "Location of Company",
                "Sector": "Sector",
                "Company_profile": "Company Profile",
                "Year": "Starting Year",
                "CIN": "Corporate Identification Number",
                "Paid_up_capital": "Paid-up Capital",
            }

            if not startup.empty:
                for idx, row in startup.iterrows():
                    result_text.tag_configure(f"startup_{idx}")
                    result_text.insert(
                        tk.END, f"Startup {idx + 1}:\n", f"startup_{idx}"
                    )
                    for column, value in row.items():
                        display_name = display_names.get(column, column)
                        result_text.insert(
                            tk.END, f"{display_name}: {value}\n", f"startup_{idx}"
                        )
                    result_text.insert(tk.END, "\n", f"startup_{idx}")
            else:
                result_text.insert(tk.END, "No startups found.\n")

        display_button = tk.Button(
            capital_frame, text="Display", command=display_min_max
        )
        display_button.pack(pady=10)
        center_window(capital_frame)

    elif selected_option == 15:   # Error. Change the code
        # Compare the Paid-up Capital of Startups with the Same Incubation Center
        compare_frame = tk.Toplevel(root)
        compare_frame.title(
            "Compare the Paid-up Capital of Startups with the Same Incubation Center"
        )

        def display_incubation_comparison():
            incubation_center = incubation_var.get()
            comparison_data = data[data["Incubation_Center"] == incubation_center]

            # Convert 'Paid_up_capital' to strings first, then remove commas
            comparison_data["Paid_up_capital"] = (
                comparison_data["Paid_up_capital"].astype(str).str.replace(",", "").astype(float)
            )

            if not comparison_data.empty:
                plt.figure(figsize=(12, 6))  # Adjust size as needed
                plt.bar(
                    comparison_data["Name_of_the_startup"],
                    comparison_data["Paid_up_capital"],
                )
                plt.xlabel("Startup Name")
                plt.ylabel("Paid-up Capital")
                plt.title(
                    f"Paid-up Capital Comparison for Startups at {incubation_center}"
                )
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                plt.show()
            else:
                print(
                    f"No startups found for the incubation center: {incubation_center}"
                )

        incubation_var = tk.StringVar()
        incubation_label = tk.Label(compare_frame, text="Select Incubation Center:")
        incubation_label.pack(padx=20, pady=10)
        cleaned_incubation_centers = [
            center.strip("', []") for center in data["Incubation_Center"].unique()
        ]

        incubation_combobox = ttk.Combobox(
            compare_frame,
            textvariable=incubation_var,
            values=cleaned_incubation_centers,
            state="normal",
            font=("Arial", 14),
        )
        incubation_combobox.pack(padx=20, pady=10)
        incubation_combobox.config(width=50)  # Adjust the width as needed

        display_button = tk.Button(
            compare_frame,
            text="Display Incubation Comparison",
            command=display_incubation_comparison,
        )
        display_button.pack(pady=10)
        center_window(compare_frame)

    elif selected_option == 16:
        incubation_count_frame = tk.Toplevel(root)
        incubation_count_frame.title("Count of Startups in Each Incubation Center")

        incubation_counts = data["Incubation_Center"].value_counts()

        result_text = tk.Text(
            incubation_count_frame,
            wrap=tk.WORD,
            height=15,
            width=70,
            state="normal",
            font=("Arial", 14),
        )
        result_text.pack(padx=20, pady=20)

        result_text.insert(tk.END, "Count of Startups in Each Incubation Center:\n\n")
        result_text.insert(tk.END, incubation_counts.to_string())
        center_window(incubation_count_frame)


# Create and place widgets
option_var = tk.IntVar(value=0)
option_label = tk.Label(root, text="Choose an option:")
option_label.pack(pady=10)

options = [
    "Display Specific Columns",
    "Sort Startups by Year",
    "Display All Starting Years of the Startup",
    "Display All Startup Names",
    "Know About the Incubation Center of Startup",
    "Know About the Location of the Startup",
    "Know About the Type of Sector of the Startup",
    "Know the Profile of the Startup",
    "Know the Corporate Identification Number of the Startup",
    "Know the Paid-up Capital of the Startup",
    "Filter the Startups Using Locations",
    "Filter the Startups Using Incubation Center",
    "Filter the Startups Using Starting Year",
    "Display the Rows with Paid-up Capital (Min|Max)",
    "Compare the Paid-up Capital of Startups with the Same Incubation Center",
    "Display the Number of Startups in Each Incubation Center",
]

for idx, option in enumerate(options, start=1):
    option_radio = tk.Radiobutton(root, text=option, variable=option_var, value=idx)
    option_radio.pack(anchor=tk.W)

analyze_button = tk.Button(root, text="Analyze", command=display_info)
analyze_button.pack(pady=20)

root.mainloop()

