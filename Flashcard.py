import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

# Create database tables if they do not exist yet or drop and recreate if necessary
def create_tables(conn):
    cursor = conn.cursor()

    # Drop the tables if they exist (be cautious, this will delete all data)
    cursor.execute('DROP TABLE IF EXISTS flashcards')
    cursor.execute('DROP TABLE IF EXISTS flashcards_sets')

    # Create flashcards_set table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS flashcards_sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create flashcards table with the correct schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            set_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            definition TEXT NOT NULL,
            FOREIGN KEY (set_id) REFERENCES flashcards_sets(id)
        )
    ''')

    conn.commit()

# Function to add a new set
def add_set(conn, name):
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO flashcards_sets (name)
        VALUES (?)
    ''', (name,))
    conn.commit()
    return cursor.lastrowid

# Function to add a flashcard to database
def add_flashcard(conn, set_id, term, definition):
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO flashcards (set_id, word, definition)
        VALUES (?, ?, ?)
    ''', (set_id, term, definition))
    conn.commit()
    return cursor.lastrowid

# Retrieve all flashcard sets from database
def get_sets(conn):
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT id, name 
        FROM flashcards_sets
    ''')
    rows = cursor.fetchall()
    return {row[1]: row[0] for row in rows}

# Retrieve all flashcards from a set
def get_flashcards(conn, set_id):
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT word, definition FROM flashcards
        WHERE set_id = ?
    ''', (set_id,))
    rows = cursor.fetchall()
    return rows

# Function to delete a set
def delete_set(conn, set_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flashcards WHERE set_id = ?', (set_id,))
    cursor.execute('DELETE FROM flashcards_sets WHERE id = ?', (set_id,))
    conn.commit()

# Add a new set
def create_set():
    set_name = set_name_var.get()
    if set_name:
        sets = get_sets(conn)
        if set_name not in sets:
            add_set(conn, set_name)
            populate_sets_combobox()
            messagebox.showinfo('Success', f'Set "{set_name}" created.')
        else:
            messagebox.showwarning('Warning', f'Set "{set_name}" already exists.')
    set_name_var.set('')

# Add a new term and definition
def add_word():
    set_name = set_name_var.get()
    term = term_var.get()
    definition = definition_var.get()

    if set_name and term and definition:
        sets = get_sets(conn)
        if set_name not in sets:
            set_id = add_set(conn, set_name)
        else:
            set_id = sets[set_name]

        add_flashcard(conn, set_id, term, definition)
        term_var.set('')
        definition_var.set('')
        populate_sets_combobox()

# Populate sets dropdown
def populate_sets_combobox():
    sets_combobox['values'] = tuple(get_sets(conn).keys())
    sets_combobox.set('')

# Select a deck to view its flashcards
def select_set():
    set_name = sets_combobox.get()
    if set_name:
        set_id = get_sets(conn)[set_name]
        cards = get_flashcards(conn, set_id)
        display_flashcards(cards)
    else:
        clear_flashcard_display()

# Display flashcards
def display_flashcards(cards):
    global current_cards, card_index
    current_cards = cards
    card_index = 0
    show_card()

# Clear flashcard display
def clear_flashcard_display():
    word_label.config(text='')
    definition_label.config(text='')

# Show current flashcard
def show_card():
    if current_cards and 0 <= card_index < len(current_cards):
        term, _ = current_cards[card_index]
        word_label.config(text=term)
        definition_label.config(text='')

# Flip the flashcard
def flip_card():
    if current_cards and 0 <= card_index < len(current_cards):
        _, definition = current_cards[card_index]
        definition_label.config(text=definition)

# Go to next card
def next_card():
    global card_index
    if current_cards and card_index < len(current_cards) - 1:
        card_index += 1
        show_card()

# Go to previous card
def prev_card():
    global card_index
    if current_cards and card_index > 0:
        card_index -= 1
        show_card()

# Main function
if __name__ == '__main__':
    # Initialize database connection
    conn = sqlite3.connect('flashcards.db')
    create_tables(conn)

    # Initialize Tkinter app
    root = tk.Tk()
    root.title('Synapse')
    root.geometry('500x400')

    # Initialize ttkbootstrap style
    style = Style(theme='superhero')

    # Initialize global variables
    current_cards = []
    card_index = 0

    # Tkinter variables
    set_name_var = tk.StringVar()
    term_var = tk.StringVar()
    definition_var = tk.StringVar()

    # Notebook for tabbed interface
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create Set Tab
    create_set_frame = ttk.Frame(notebook)
    notebook.add(create_set_frame, text='Create New Deck')

    ttk.Label(create_set_frame, text='Deck Name:').pack(padx=10, pady=5)
    ttk.Entry(create_set_frame, textvariable=set_name_var).pack(pady=5)

    ttk.Label(create_set_frame, text='Term:').pack(padx=10, pady=5)
    ttk.Entry(create_set_frame, textvariable=term_var).pack(pady=5)

    ttk.Label(create_set_frame, text='Definition:').pack(padx=10, pady=5)
    ttk.Entry(create_set_frame, textvariable=definition_var).pack(pady=5)

    ttk.Button(create_set_frame, text='Add Term', command=add_word).pack(pady=5)
    ttk.Button(create_set_frame, text='Save Deck', command=create_set).pack(pady=5)

    # Select Set Tab
    select_set_frame = ttk.Frame(notebook)
    notebook.add(select_set_frame, text='Select Deck')

    sets_combobox = ttk.Combobox(select_set_frame, state='readonly')
    sets_combobox.pack(pady=20)
    ttk.Button(select_set_frame, text='Select Deck', command=select_set).pack(pady=5)
    ttk.Button(select_set_frame, text='Delete Deck', command=lambda: delete_set(conn, get_sets(conn).get(sets_combobox.get(), -1))).pack(pady=5)

    # Learning Mode Tab
    learning_mode_frame = ttk.Frame(notebook)
    notebook.add(learning_mode_frame, text='Learning Mode')

    word_label = ttk.Label(learning_mode_frame, font=('TkPoppins', 24))
    word_label.pack(pady=10)

    definition_label = ttk.Label(learning_mode_frame, font=('TkPoppins', 18))
    definition_label.pack(pady=10)

    ttk.Button(learning_mode_frame, text='Flip Card', command=flip_card).pack(side='left', padx=5)
    ttk.Button(learning_mode_frame, text='Previous Card', command=prev_card).pack(side='left', padx=5)
    ttk.Button(learning_mode_frame, text='Next Card', command=next_card).pack(side='left', padx=5)

    # Populate dropdown with sets
    populate_sets_combobox()
    root.mainloop()
