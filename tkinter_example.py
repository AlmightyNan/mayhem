import tkinter as tk


class SimpleApp:
    def create_widgets():
        root = tk.Tk()
        root.title('aunty pudinguruchu aunty!!!!')
        root.geometry("600x400")
        label = tk.Label(root, text="Enter two numbers:", font=('Montserrat', 16))
        label.pack()

        entry1 = tk.Entry(root)
        entry1.pack()

        entry2 = tk.Entry(root)
        entry2.pack()

        result_label = tk.Label(root, text="")
        result_label.pack()

        def perform_addition():
            num1 = float(entry1.get())
            num2 = float(entry2.get())
            result = num1 + num2
            result_label.config(text="Result: " + str(result))

        def perform_subtraction():
            num1 = float(entry1.get())
            num2 = float(entry2.get())
            result = num1 - num2
            result_label.config(text="Result: " + str(result))

        add_button = tk.Button(root, text="Add", command=perform_addition)
        add_button.pack()

        sub_button = tk.Button(root, text="Subtract", command=perform_subtraction)
        sub_button.pack()

        root.mainloop()

    def run():
        SimpleApp.create_widgets()


SimpleApp.run()
