from tkinter import Tk
import classes as cls
import functions as fn



def main():
    print("Welcome to Lexihone!")
    root = Tk()
    root.title("Lexihone")
    root.resizable(False, False)
    root.configure(background='#31363b')
    f_name = fn.get_filename()

    myapp = cls.UI(root, f_name)
    root.mainloop()

if __name__ == '__main__':
    main()
