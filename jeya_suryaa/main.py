import pandas as pd
import matplotlib.pyplot as plt
import random as rd
import curses 

def plot_stock_data(data, company_name):
    selected_companies = data[data.index.str.contains(company_name, case=False, na=False)]
    
    if not selected_companies.empty:
        selected_company = selected_companies.iloc[0]
        selected_data = selected_company[2:7].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else x)
        selected_data.plot(kind='bar', title=selected_company.name, color=['black', 'purple', 'black', 'purple', 'black'])
        plt.xticks(rotation=45)
        plt.show()
    else:
        print("No matching companies found.")

def plot_mean_data(data):
    random_companies = rd.sample(data.index.tolist(), 5)
    random_data = data.loc[random_companies, 'Open':'Adj Close'].applymap(lambda x: float(x.replace(',', '').replace('"', '')) if isinstance(x, str) else x)
    
    for index, row in random_data.iterrows():
        plt.plot(row.index, row.values, marker='o', label=index)
    
    plt.xlabel('Attributes')
    plt.ylabel('Values')
    plt.title("Stock Data of Random Companies")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def show_credits(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height//2 - 1, width//2 - len("Credits & Project Info:")//2, "Credits & Project Info:")
    stdscr.attroff(curses.color_pair(3))
    
    # Set text color to green
    stdscr.attron(curses.color_pair(4))
    credits_text = """Created by: Jeyasuryaa V"""
    stdscr.addstr(height//2, width//2 - len(credits_text)//2, credits_text)
    stdscr.attroff(curses.color_pair(4))
    
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Selected option color pair
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)  # Highlighted text color pair
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Title color pair
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green text color pair

    # Rest of your code
    
    options = [
        "Analyze stock data for a specific company",
        "Plot stock data of random companies",
        "Credits & Project Info",
        "Exit"
    ]

    selected_option = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(1, width//2 - len("Stock Data Analysis")//2, "Stock Data Analysis")
        stdscr.addstr(1, width//2 - len("Use up ↑ and down ↓ keys to navigate to options")//2, "Use up ↑ and down ↓ keys to navigate to options")
        stdscr.attroff(curses.color_pair(3))
        
        for i, option_text in enumerate(options):
            if i == selected_option:
                stdscr.addstr(height//2 - len(options)//2 + i, width//2 - len(option_text)//2 - 2, '> ' + option_text, curses.color_pair(1))
            else:
                stdscr.addstr(height//2 - len(options)//2 + i, width//2 - len(option_text)//2 - 2, '  ' + option_text)
        
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == 10:  # Enter key
            selected_option_text = options[selected_option]
            if selected_option_text == "Analyze stock data for a specific company":
                stdscr.clear()
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(height//2 - 1, width//2 - len("Enter company name: ")//2, "Enter company name: ")
                stdscr.attroff(curses.color_pair(2))
                stdscr.refresh()
                curses.echo()
                company_name = stdscr.getstr().decode().strip().lower()
                curses.noecho()
                plot_stock_data(s, company_name)
            elif selected_option_text == "Plot stock data of random companies":
                plot_mean_data(s)
            elif selected_option_text == "Credits & Project Info":
                show_credits(stdscr)
            elif selected_option_text == "Exit":
                break

if __name__ == "__main__":
    curses.wrapper(main)