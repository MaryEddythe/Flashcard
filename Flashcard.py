import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

if __name__ == '__main__':

    # create now the main gui
    root = tk.Tk()
    root.title('Synapse')
    root.geometry('500x400')
    
    # styling sang gui
    style = Style(theme='superhero')
    style.configure('Tlabel', font = ('TkPoppins', 18))
    style.configure('Tlabel', font = ('TkPoppins', 16))

    # variables to store user input
    set_name_var = tk.StringVar()
    word_var = tk.StringVar()
    definition_var = tk.StringVar()

    #notebook widget to manage tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    #para sa create new set nga tab
    create_set_frame = ttk.Frame(notebook)
    notebook.add(create_set_frame, text='Create New Deck')

    #label and entry widgets for entering set name, word and definition 
    set_name_label = ttk.Label(create_set_frame, text='Deck Name:').pack(side='left', padx=(10, 0))
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(padx=5, pady=5)
    
    set_name_label = ttk.Label(create_set_frame, text='Term:').pack(side='left', padx=(0, 10))
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(padx=5, pady=5)

    set_name_label = ttk.Label(create_set_frame, text='Definition:').pack(side='left', padx=(0, 10))
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(padx=5, pady=5)

    #buttons to add word sa deck (command=add_word) 
    ttk.Button(create_set_frame, text= 'Add Term').pack(padx=5, pady=5)

    #buttons para mag save ang deck (command=save_deck)
    ttk.Button(create_set_frame, text= 'Save Deck').pack(padx=10, pady=10)

    #Create select "select tab" and its contents
    select_set_frame = ttk.Frame(notebook)   
    notebook.add(select_set_frame, text="Select Deck")

    #combo box for selecting widget sets


    # Connect to SQLite database
    root.mainloop()

