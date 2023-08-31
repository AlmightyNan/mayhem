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

def main():
    s = pd.read_csv('stock analysis.csv')  # Change the file name to match your CSV file
    s.index = ["Reliance Industries", "Tata Steel", "Tata Motors", "HFCL", "ITC", "Adani Power", "NIFTY", "Apollo Micro Systems Ltd",
               "Reliance BP Mobility Ltd", "DJI", "Google", "Microsoft", "Apple", "Tesla", "SpaceX", "Bayerische Motoren Werke AG",
               "Mercedes Benz Group AG", "Adidas AG", "Vedanta Ltd", "Alembic Ltd", "Meta Platforms Inc", "Infosys Ltd", "IBM Common Stock",
               "Tata Consultancy Services Ltd", "Hindustan Unilever Ltd", "Aditya Birla Money Ltd", "Aditya Birla Capital Ltd", "Sony Group Corp",
               "Maruti Suzuki India Ltd", "Hero Motocorp Ltd"]

    pd.set_option('display.max_columns', None)

    print("Welcome to Stock Data Analysis")

    while True:
        print("\nOptions:")
        print("1. Analyze stock data for a specific company")
        print("2. Plot stock data of random companies")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            print('To represent the elements of the stock market of a company')
            company_name = input('Enter company name: ').strip().lower()
            plot_stock_data(s, company_name)
        elif choice == '2':
            plot_mean_data(s)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
