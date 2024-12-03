import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

# Create database tables if they do not exist yet
def create_tables(conn):
    cursor = conn.cursor()

    # Create flashcards_set table if it does not exist
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flashcards_sets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                    )
             ''')
    
    # Flashcards table with foreign key
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flashcards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        set_id INTEGER NOT NULL,
                        definition TEXT NOT NULL,
                        FOREIGN KEY (set_id) REFERENCES flashcards_sets(id)
                    )
             ''')
    
    conn.commit()

# Function to add a new set
def add_set(conn, name):
    cursor = conn.cursor()
    
    # Insert flashcard set name to the table
    cursor.execute('''
                   INSERT INTO flashcards_sets (name)
                   VALUES (?)
            ''', (name,))
    
    set_id = cursor.lastrowid
    conn.commit()

    return set_id






















# Main function
if __name__ == '__main__':
    # Connect to SQLite database and create tables
    conn = sqlite3.connect('flashcards.db')
    create_tables(conn)

    # Create the main GUI
    root = tk.Tk()
    root.title('Synapse')
    root.geometry('500x400')
    
    # Styling the GUI
    style = Style(theme='superhero')
    style.configure('TLabel', font=('TkPoppins', 16))

    # Variables to store user input
    set_name_var = tk.StringVar()
    term_var = tk.StringVar()
    definition_var = tk.StringVar()

    # Notebook widget to manage tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create new set tab
    create_set_frame = ttk.Frame(notebook)
    notebook.add(create_set_frame, text='Create New Deck')

    # Label and entry widgets for entering set name, word, and definition 
    ttk.Label(create_set_frame, text='Deck Name:').pack(side='top', padx=(10, 0))
    ttk.Entry(create_set_frame, textvariable=set_name_var, width=30).pack(padx=5, pady=5)
    
    ttk.Label(create_set_frame, text='Term:').pack(side='top', padx=(0, 10))
    ttk.Entry(create_set_frame, textvariable=term_var, width=30).pack(padx=5, pady=5)

    ttk.Label(create_set_frame, text='Definition:').pack(side='top', padx=(0, 10))
    ttk.Entry(create_set_frame, textvariable=definition_var, width=30).pack(padx=5, pady=5)

    # Buttons to add word and save deck
    ttk.Button(create_set_frame, text='Add Term').pack(padx=5, pady=5)
    ttk.Button(create_set_frame, text='Save Deck').pack(padx=10, pady=10)

    # Select deck tab
    select_set_frame = ttk.Frame(notebook)   
    notebook.add(select_set_frame, text="Select Deck")

    # Combo box for selecting widget sets
    sets_combobox = ttk.Combobox(select_set_frame, state='readonly')
    sets_combobox.pack(padx=5, pady=40)

    # Buttons for selecting, deleting, and editing sets
    ttk.Button(select_set_frame, text='Select Deck').pack(padx=5, pady =5)
    ttk.Button(select_set_frame, text='Delete Deck').pack(padx=5, pady=5)
    ttk.Button(select_set_frame, text='Edit Deck').pack(padx=5, pady=5)

    # Learning mode frame
    learning_mode_frame = ttk.Frame(notebook)
    notebook.add(learning_mode_frame, text='Learning Mode')

    # Initializing variables for tracking index and current cards
    current_index = 0
    current_card = []

    # Label display of words on flashcards
    word_label = ttk.Label(learning_mode_frame, textvariable=term_var, font=('TkPoppins', 24))
    word_label.pack(pady=5)

    # Buttons for next and previous cards
    # ttk.Button(learning_mode_frame, text='Previous', command=lambda: previous_card()).pack(side='left', padx=5)
    # ttk.Button(learning_mode_frame, text='Next', command=lambda: next_card()).pack(side='right', padx=5)

    # Label for displaying the definition
    definition_label = ttk.Label(learning_mode_frame, textvariable=definition_var, font=('TkPoppins', 18))
    definition_label.pack(pady=5, padx=5)

    # Button to flip the cards
    ttk.Button(learning_mode_frame, text='Flip Card').pack(side='left', padx=5, pady=5)

    # Button to view next card of the deck
    ttk.Button(learning_mode_frame, text='Next Card').pack(side='right', padx=5)

    # Button to view previous card of the deck
    ttk.Button(learning_mode_frame, text='Previous Card').pack(side='right', padx=5, pady=5)

    # Connect to SQLite database
    root.mainloop()