import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk

def on_matplotlib_close(event):
    plt.close()
    open_tkinter_window()

def open_tkinter_window():
    root = tk.Tk()
    root.title("...")
    root.geometry("800x600")
    root.configure(bg="#ffc404")

    image = Image.open("/home/almightynan/Desktop/mayhem/mayhem/draco_aathi/csk.jpg")
    image = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=image, bg="#ffc404")
    image_label.image = image
    image_label.pack(fill=tk.BOTH, expand=True)

    thank_you_label = tk.Label(root, text="Thank You", bg="#ffc404", font=('Montserrat', 30))
    thank_you_label.pack(pady=(0, 20))

    def destroy_window():
        root.destroy()

    button = tk.Button(root, text="Exit this window", command=destroy_window, font=('Montserrat', 14))
    button.pack(pady=(0, 10))

    root.mainloop()

d=pd.read_csv('/home/almightynan/Desktop/mayhem/mayhem/draco_aathi/dataset.csv')
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
print(d)
print('Want To Filter Data Or Analyse The Data')
print('1.Filtering Data \n2.Anaylsing Data')
e=int(input('Enter The Option(1 or 2):'))
if e==1:
    print('Want To Filter Using :')
    print('1.Venue \n2.Opponent \n3.Man Of The Match')
    a=int(input('Enter The Option(1 or 2 or 3):'))
    if a==1:
        print('The Venues Are :')
        print('1.Chennai \n2.Bangalore \n3.Mumbai \n4.Gujarat \n5.Mohali \n6.Hyderabad \n7.Kolkata \n8.Ahmedabad \n9.Nagpur \n10.Kochi \n11.Dharamsala \n12.Pune \n13.Dubai \n14.Abu Dhabi \n15.Sharjah')
        b=int(input('Enter The Option(1-15):'))
        if b==1:
            print('Matches Held In Chennai Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Chennai ',['Date & Year','Venue','Opponent','Result']])
        if b==2:
            print('Matches Held In Bangalore Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Bangalore',['Date & Year','Venue','Opponent','Result']])
        if b==3:
            print('Matches Held In Mumbai Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Mumbai',['Date & Year','Venue','Opponent','Result']])
        if b==4:
            print('Matches Held In Gujarat Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Gujarat',['Date & Year','Venue','Opponent','Result']])
        if b==5:
            print('Matches Held In Mohali Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Mohali',['Date & Year','Venue','Opponent','Result']])
        if b==6:
            print('Mathches Held In Hyderabad Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Hyderabad',['Date & Year','Venue','Opponent','Result']])
        if b==7:
            print('Matches Held In Kolkata Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Kolkata',['Date & Year','Venue','Opponent','Result']])
        if b==8:
            print('Mathches Held In Ahmedabad Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Ahmedabad',['Date & Year','Venue','Opponent','Result']])
        if b==9:
            print('Mathches Held In Nagpur Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Nagpur',['Date & Year','Venue','Opponent','Result']])
        if b==10:
            print('Matches Held In Kochi Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Kochi',['Date & Year','Venue','Opponent','Result']])
        if b==11:
            print('Mathches Held In Dharamsala Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Dharamsala',['Date & Year','Venue','Opponent','Result']])
        if b==12:
            print('Matches Held In Pune Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Pune',['Date & Year','Venue','Opponent','Result']])
        if b==13:
            print('Matches Held In Dubai Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Dubai',['Date & Year','Venue','Opponent','Result']])
        if b==14:
            print('Matches Held In Abu Dhabi Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Abu Dhabi',['Date & Year','Venue','Opponent','Result']])
        if b==15:
            print('Matches Held In Sharjah Are ')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Venue']=='Sharjah',['Date & Year','Venue','Opponent','Result']])    
    if a==2:
        print('The Opponent Teams Are:')
        print('1.Kings Xl Punjab \n2.Mumbai Indians \n3.Kolkata Knight Riders \n4.Royal Challangers Bangalore \n5.Delhi Daredevils ')
        print('6.Rajasthan Royals \n7.Deccan Chargers \n8.Pune Warriors India \n9.Kochi Tuskers Kerala \n10.Sunrises Hyderabad \n11.Delhi Capitals \n12.Lucknow Super Giants \n13.Gujarat Titans')
        c=int(input('Enter The Option(1-13):'))
        if c==1:
            print('Matches Vs Kings XI Punjab')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Kings Xl Punjab',['Date & Year','Opponent','Result']])
        if c==2:
            print('Matches Vs Mumbai Indians')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Mumbai Indians ',['Date & Year','Opponent','Result']])
        if c==3:
            print('Matches Vs Kolkata Knight Riders')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Kolkata Knight Riders',['Date & Year','Opponent','Result']])
        if c==4:
            print('Mathches Vs Royal Challangers Bangalore')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Royal Challangers Bangalore',['Date & Year','Opponent','Result']])
        if c==5:
            print('Matches Vs Delhi Daredevils')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Delhi Daredevils ',['Date & Year','Opponent','Result']])
        if c==6:
            print('Matches Vs Rajasthan Royals')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Rajasthan Royals ',['Date & Year','Opponent','Result']])
        if c==7:
            print('Matches Vs Deccan Chargers')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Deccan Chargers ',['Date & Year','Opponent','Result']])
        if c==8:
            print('Matches Vs Pune Warriors India')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Pune Warriors India',['Date & Year','Opponent','Result']])
        if c==9:
            print('Mathches Vs Kochi Tuskers Kerala')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Kochi Tuskers Kerala',['Date & Year','Opponent','Result']])
        if c==10:
            print('Matches Vs Sunrises Hyderabad')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Sunrises Hyderabad',['Date & Year','Opponent','Result']])
        if c==11:
            print('Mathches Vs Delhi Capitals')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Delhi Capitals',['Date & Year','Opponent','Result']])
        if c==12:
            print('Matches Vs Lucknow Super Giants')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Lucknow Super Giants',['Date & Year','Opponent','Result']])
        if c==13:
            print('Matches Vs Gujarat Titans')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Opponent']=='Gujarat Titans',['Date & Year','Opponent','Result']])    
    if a==3:
        print('The Players Are:')
        print('1.Mahedra Singh Dhoni \n2.Ravindra Jadeja \n3.Micheal Hussey \n4.Virender Sehwag \n5.Suresh Raina \n6.Ab de Villiers \n7.Faf du Plessis\n8.Virat Kohli \n9.Kieron Pollard \n10.Dwayne Smith \n11.Devon Conway \n12.Ruturaj Gaikwad \n13.Sachin Tendulkar \n14.Rohit Sharma \n15.Hardik Pandya \n16.Dwayne Bravo \n17.Shane Watson \n18.Ambati Rayudu \n19.Ravichandran Ashwin \n20.Chris Gayle')
        m=int(input('Enter The Option(1-20):'))
        if m==1:
            print('Mahedra Singh Dhoni\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Dhoni ',['Date & Year','Opponent','Result']])
        if m==2:
            print('Ravindra Jadeja\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Jadeja',['Date & Year','Opponent','Result']])
        if m==3:
            print('Micheal Hussey\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Hussey',['Date & Year','Opponent','Result']])
        if m==4:
            print('Virender Sehwag\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Sehwag',['Date & Year','Opponent','Result']])
        if m==5:
            print('Suresh Raina\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Raina',['Date & Year','Opponent','Result']])
        if m==6:
            print('Ab de Villiers\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Ab d',['Date & Year','Opponent','Result']])
        if m==7:
            print('Faf du Plessis\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Faf',['Date & Year','Opponent','Result']])
        if m==8:
            print('Virat Kohli\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Kohli',['Date & Year','Opponent','Result']])
        if m==9:
            print('Kieron Pollard\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Pollard',['Date & Year','Opponent','Result']])
        if m==10:
            print('Dwayne Smith\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='D Smith',['Date & Year','Opponent','Result']])
        if m==11:
            print('Devon Conway\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Conway',['Date & Year','Opponent','Result']])
        if m==12:
            print('Ruturaj Gaikwad\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Gaikwad',['Date & Year','Opponent','Result']])   
        if m==13:
            print('Sachin Tendulkar\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Sachin',['Date & Year','Opponent','Result']])     
        if m==14:
            print('Rohit Sharma\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Rohit',['Date & Year','Opponent','Result']])     
        if m==15:
            print('Hardik Pandya\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Hardik',['Date & Year','Opponent','Result']])     
        if m==16:
            print('Dwayne Bravo\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Bravo',['Date & Year','Opponent','Result']])
        if m==17:
            print('Shane Watson\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Watson',['Date & Year','Opponent','Result']])
        if m==18:
            print('Ambati Rayudu\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Rayudu',['Date & Year','Opponent','Result']])
        if m==19:
            print('Ravichandran Ashwin\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Ashwin',['Date & Year','Opponent','Result']])
        if m==20:
            print('Chris Gayle\'s Man Of The Matches :')
            pd.set_option('display.max_rows',None)
            print(d.loc[d['Man of the match']=='Gayle',['Date & Year','Opponent','Result']])
if e==2:
    print('Want To Analyse :')
    print('1.Pie Chart')
    print('2.Bar Graph')
    z=int(input('Enter The Option:'))
    if z==1:
        print('Data Analyse the Pie Chart by using Teams:')
        print('1.Royal Challangers Bangalore \n2.Mumbai Indians \n3.Kolkata Knight Riders \n4.Gujart Titans \n5.Lucknow Super Giants \n6.Kings Xl Punjab \n7.Sunrises Hyderabad \n8.Delhi Capitals \n9.Rajasthan Royals')
        c=int(input('Enter The Option(1-9):'))
        if c==1:
            contri=[19,10,1]
            Team1=['CSK','RCB','MA']
            Clr=['yellow','red','silver']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==2:
            contri=[15,18]
            Team1=['CSK','MI',]
            Clr=['yellow','blue']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==3:
            contri=[18,10,1]
            Team1=['CSK','KKR','MA']
            Clr=['yellow','violet','silver']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==4:
            contri=[2,3]
            Team1=['CSK','GT',]
            Clr=['yellow','blue']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==5:
            contri=[1,1,1]
            Team1=['CSK','LSG','MA']
            Clr=['yellow','blue','silver']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==6:
            contri=[14,11,]
            Team1=['CSK','KXIP',]
            Clr=['yellow','red',]
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==7:
            contri=[14,5]
            Team1=['CSK','SRH',]
            Clr=['yellow','orange']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==8:
            contri=[19,9]
            Team1=['CSK','DC',]
            Clr=['yellow','blue']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if c==9:
            contri=[15,12]
            Team1=['CSK','RR',]
            Clr=['yellow','pink']
            plt.pie(contri,labels=Team1,colors=Clr,autopct='%1.1f%%')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
    if z==2:
        print('Data Analyse The Graph Of :')
        print('1.Matches VS Year')
        print('2.Matches VS Opponent')
        print('3.Result')
        v=int(input('Enter The Option :'))
        if v==1:
            l=[len(d.loc[d['Date & Year'].str.contains('2008')]),len(d.loc[d['Date & Year'].str.contains('2009')]),len(d.loc[d['Date & Year'].str.contains('2010')]),len(d.loc[d['Date & Year'].str.contains('2011')]),len(d.loc[d['Date & Year'].str.contains('2012')]),len(d.loc[d['Date & Year'].str.contains('2013')]),len(d.loc[d['Date & Year'].str.contains('2014')]),len(d.loc[d['Date & Year'].str.contains('2015')]),len(d.loc[d['Date & Year'].str.contains('2016')]),len(d.loc[d['Date & Year'].str.contains('2017')]),len(d.loc[d['Date & Year'].str.contains('2018')]),len(d.loc[d['Date & Year'].str.contains('2019')]),len(d.loc[d['Date & Year'].str.contains('2020')]),len(d.loc[d['Date & Year'].str.contains('2021')]),len(d.loc[d['Date & Year'].str.contains('2022')]),len(d.loc[d['Date & Year'].str.contains('2023')])]
            plt.plot(l,'gold',marker='o',markerfacecolor='k')
            plt.title('Matches VS Year')
            plt.xlabel('Year')
            plt.ylabel('No.Of.Matches')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if v==2:
            l=[len(d.loc[d['Opponent']=='Royal Challangers Bangalore']),len(d.loc[d['Opponent']=='Kings Xl Punjab']),len(d.loc[d['Opponent']=='Mumbai Indians ']),len(d.loc[d['Opponent']=='Kolkata Knight Riders']),len(d.loc[d['Opponent']=='Delhi Daredevils ']),len(d.loc[d['Opponent']=='Rajasthan Royals ']),len(d.loc[d['Opponent']=='Deccan Chargers ']),len(d.loc[d['Opponent']=='Pune Warriors India']),len(d.loc[d['Opponent']=='Kochi Tuskers Kerala']),len(d.loc[d['Opponent']=='Sunrises Hyderabad']),len(d.loc[d['Opponent']=='Delhi Capitals']),len(d.loc[d['Opponent']=='Lucknow Super Giants']),len(d.loc[d['Opponent']=='Gujarat Titans'])]
            x=['RCB','KXIP','MI','KKR','DD','RR','DEC','PWI','KTK','SRH','DC','LSG','GT']
            plt.bar(x,l,color=['red','pink','blue','blueviolet','orangered','hotpink','navy','magenta','dodgerblue','orange','green','aqua','grey'])
            plt.title('Matches VS Opponent')
            plt.xlabel('Opponent')
            plt.ylabel('No.Of.Matches')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
        if v==3:
            l=[len(d.loc[d['Result'].str.contains('Won')]),len(d.loc[d['Result'].str.contains('Lost')])]
            x=['WON','LOST']
            plt.bar(x,l,color=['gold','black'])
            plt.title('Result VS Matches')
            plt.xlabel('Result')
            plt.ylabel('No.Of.Matches')
            plt.gcf().canvas.mpl_connect("close_event", on_matplotlib_close)
            plt.show()
print('நன்றி மீண்டும் வருக')