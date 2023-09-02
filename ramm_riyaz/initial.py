import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

X = pd.read_csv("/home/almightynan/Downloads/st.csv", index_col="Rows")
pd.set_option("display.max_columns", None)

q = input("Want To Access Data (y|n):")

if q == "y":
    print("1) To display the Specific Columns.")
    print("2) To display All starting Year of the Startup.")
    print("3) To display All Startup Name.")
    print("4) To know about the Incubation Center of Startup.")
    print("5) To know about the Location of the Startup.")
    print("6) To know about the type of Sector of the Startup.")
    print("7) To know the profile of the Startup.")
    print("8) To know the Corporate Identification Number of the Startup.")
    print("9) To know  the Paid-up capital of the Startup.")
    print("10) To filter the Startups using Locations.")
    print("11) To filter the Startups using Incubation Center.")
    print("12) To filter the Startups using Starting Year.")
    print("13) To display the row which has Paid-up capital (Min|Max).")
    print("14) To compare the Paid up capital of all Startups(Line Graph).")

A = int(input("Enter value to Analyse Data (1-16):"))

if A == 1:
    aa = int(input("Enter the number of columns You want to display(1-4):"))
    print("To refer the Column Names:\n", X.columns)
    if aa == 1:
        a1 = input("Name of the column:")
        print(X.loc[:, a1])

    elif aa == 2:
        a2_1 = input("Name of the First Column:")
        a2_2 = input("Name of the Second Column:")
        print(X.loc[:, [a2_1, a2_2]])

    elif aa == 3:
        a3_1 = input("Name of the First Column:")
        a3_2 = input("Name of the Second Column:")
        a3_3 = input("Name of the Third Column:")
        print(X.loc[:, [a3_1, a3_2, a3_3]])

    elif aa == 4:
        a4_1 = input("Name of the First Column:")
        a4_2 = input("Name of the Second Column:")
        a4_3 = input("Name of the Third Column:")
        a4_4 = input("Name of the Fourth Column:")
        print(X.loc[:, [a4_1, a4_2, a4_3, a4_4]])

if A == 2:
    a = input("To display in Ascending order or Decending order[A|D]:")

    if a == "A":
        pd.set_option("display.max_columns", None)
        print(X.sort_values(by=["Year"]))
    if a == "D":
        pd.set_option("display.max_columns", None)
        print(X.sort_values(by=["Year"], ascending=False))

elif A == 3:
    b = input("To display in Ascending order or Decending order[A|D]:")

    if b == "A":
        pd.set_option("display.max_columns", None)
        print(X.sort_values(by=["Name_of_the_startup"]))
    if b == "D":
        pd.set_option("display.max_columns", None)
        print(X.sort_values(by=["Name_of_the_startup"], ascending=False))

elif A == 4:
    c = input("Name of the Startup:")
    c1 = X.Incubation_Center[X.Name_of_the_startup == c]
    print("The Incubation Center of", c, "is", list(c1))

elif A == 5:
    d = input("Name of the Startup:")
    d1 = X.Location_of_company[X.Name_of_the_startup == d]
    print("The Location of startup of", d, "is in", list(d1))

elif A == 6:
    e = input("Name of the Startup:")
    e1 = X.Sector[X.Name_of_the_startup == e]
    print("The Sector of startup of", e, "is", list(e1))

elif A == 7:
    f = input("Name of the Startup:")
    f1 = X.Company_profile[X.Name_of_the_startup == f]
    print("The Profile of startup of", f, "is ", list(f1))

elif A == 8:
    g = input("Name of the Startup:")
    g1 = X.CIN[X.Name_of_the_startup == g]
    print("The Corporate Identification Number of startup of", g, "is ", list(g1))

elif A == 9:
    i = input("Name of the Startup:")
    i1 = X.Paid_up_capital[X.Name_of_the_startup == i]
    print("The Corporate Paid-up capital of startup of", i, "is ", list(i1))

elif A == 10:
    h = input("Name of the City(ex: Chennai,Delhi,Mumbai,Bengaluru):")
    h1 = X.Name_of_the_startup[X.Location_of_company == h]
    print(h1)

elif A == 11:
    j = input("Name of the Incubation Center:")
    j1 = X.Name_of_the_startup[X.Incubation_Center == j]
    print(j1)

elif A == 12:
    l = int(input("Starting Year(2017-2021):"))
    l1 = X.Name_of_the_startup[X.Year == l]
    print(l1)

elif A == 13:
    k = input("Row which has high or low Paid-up capital(Min | Max):")
    if k == "Min":
        k1 = np.array(X.Paid_up_capital)
        print(X[X.Paid_up_capital == np.min(k1)])

    elif k == "Max":
        k2 = np.array(X.Paid_up_capital)
        print(X[X.Paid_up_capital == np.max(k2)])


elif A == 14:
    print("The Graph is:")

    plt.xlabel("Name of The Startups")
    plt.ylabel("Paid up capital")
    plt.bar(list(X.Name_of_the_startup), list(X.Paid_up_capital), width=0.20)
    plt.show()
