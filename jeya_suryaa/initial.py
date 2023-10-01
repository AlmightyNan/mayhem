import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rd

s=pd.read_csv('stock analysis.csv')
pd.set_option('display.max_columns',None)
j=input('Enter (YES|NO) To Analyse the Data:')
while True:
    if j=='yes':
        print('To represent the elements of the stock market of a company')
        b=input('Enter company name:')
        if b=="reli":
            x = s.iloc[[0],:]
            print(x)
            plt.plot(s.iloc[0,2:])
            plt.show()
        if b=="tast":
           a = s.iloc[[1],:]
           print(a)
           plt.plot(s.iloc[1,2:])
           plt.show()
        if b=="tamo":
           c = s.iloc[[2],:]
           print(c)
           plt.plot(s.iloc[2,2:])
           plt.show()
        if b=="hfcl":
           d = s.iloc[[3],:]
           print(d)
           plt.plot(s.iloc[3,2:])
           plt.show()
        if b=="itc":
           e = s.iloc[[4],:]
           print(e)
           plt.plot(s.iloc[4,2:])
           plt.show()
        if b=="adpo":
           f = s.iloc[[5],:]
           print(f)
           plt.plot(s.iloc[5,2:])
           plt.show()
        if b=="nifty":
           g= s.iloc[[6],:]
           print(g)
           plt.plot(s.iloc[6,2:])
           plt.show()
        if b=="apollo":
           h= s.iloc[[7],:]
           print(h)
           plt.plot(s.iloc[7,2:])
           plt.show()
        if b=="relibp":
           i = s.iloc[[8],:]
           print(i)
           plt.plot(s.iloc[8,2:])
           plt.show()
        if b=="dji":
           g1 = s.iloc[[9],:]
           print(g1)
           plt.plot(s.iloc[9,2:])
           plt.show()
        if b=="google":
            k = s.iloc[[10],:]
            print(k)
            plt.plot(s.iloc[10,2:])
            plt.show()
        if b=="ms":
           l = s.iloc[[11],:]
           print(l)
           plt.plot(s.iloc[11,2:])
           plt.show()
        if b=="apple":
           m = s.iloc[[12],:]
           print(m)
           plt.plot(s.iloc[12,2:])
           plt.show()
        if b=="tesla":
           n = s.iloc[[13],:]
           print(n)
           plt.plot(s.iloc[13,2:])
           plt.show()
        if b=="spacex":
           o = s.iloc[[14],:]
           print(o)
           plt.plot(s.iloc[14,2:])
           plt.show()
        if b=="bmw":
           p = s.iloc[[15],:]
           print(p)
           plt.plot(s.iloc[15,2:])
           plt.show()
        if b=="benz":
           q = s.iloc[[16],:]
           print(q)
           plt.plot(s.iloc[16,2:])
           plt.show()
        if b=="adidas":
           r = s.iloc[[17],:]
           print(r)
           plt.plot(s.iloc[17,2:])
           plt.show()
        if b=="vedanta":
           y = s.iloc[[18],:]
           print(y)
           plt.plot(s.iloc[18,2:])
           plt.show()
        if b=="alembic":
           t = s.iloc[[19],:]
           print(t)
           plt.plot(s.iloc[19,2:])
           plt.show()
        if b=="meta":
           u = s.iloc[[20],:]
           print(u)
           plt.plot(s.iloc[20,2:])
           plt.show()
        if b=="infosys":
           v = s.iloc[[21],:]
           print(v)
           plt.plot(s.iloc[21,2:])
           plt.show()
        if b=="ibm":
           w = s.iloc[[22],:]
           print(w)
           plt.plot(s.iloc[22,2:])
           plt.show()
        if b=="tcs":
           f1 = s.iloc[[23],:]
           print(f1)
           plt.plot(s.iloc[23,2:])
           plt.show()
        if b=="hul":
           z = s.iloc[[24],:]
           print(z)
           plt.plot(s.iloc[24,2:])
           plt.show()
        if b=="birla money":
           a1 = s.iloc[[25],:]
           print(a1)
           plt.plot(s.iloc[25,2:])
           plt.show()
        if b=="birla cap":
           b1 = s.iloc[[26],:]
           print(b1)
           plt.plot(s.iloc[26,2:])
           plt.show()
        if b=="sony":
           c1 = s.iloc[[27],:]
           print(c1)
           plt.plot(s.iloc[27,2:])
           plt.show()
        if b=="Maruthi":
           d1 = s.iloc[[28],:]
           print(d1)
           plt.plot(s.iloc[28,2:])
           plt.show()
        if b=="hero":
           e1 = s.iloc[[29],:]
           print(e1)
           plt.plot(s.iloc[29,2:])
           plt.show()

i1=rd.sample(["Reliance Industries"," Tata Steel", "Tata Mortors", "HFCL", "ITC", "Adani Power", "NIFTY", "Apollo Micro Systems Ltd",
         "Reliance BP Mobility Ltd", "DJI"," Google", "Microsoft", "Apple", "Tesla", "SpaceX", "Bayerische Motoren Werke AG",
         "Mercedes Benz Group AG", "Adidas AG", "Vedanta Ltd", "Alembic Ltd", "Meta Platforms Inc", "Infosys Ltd", "IBM Common Stock",
        "Tata Consultancy Services Ltd","Hindustan Unilever Ltd", "Aditya Birla Money Ltd", "Aditya Birla Capital Ltd", "Sony Group Corp",
       "Maruti Suzuki India Ltd", "Hero Motocorp Ltd"], 5)
#h1 = s[s.index.str.contains(search_query, case=False, na=False)].iloc[0]
j1=s.loc[i1, 2:]
plt.bar(j1)
plt.show()