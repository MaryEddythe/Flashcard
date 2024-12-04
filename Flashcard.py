import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

# Database setup
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS flashcards')
    cursor.execute('DROP TABLE IF EXISTS flashcards_sets')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS flashcards_sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
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

# Helper functions
def add_set(conn, name):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flashcards_sets (name) VALUES (?)', (name,))
    conn.commit()
    return cursor.lastrowid

def add_flashcard(conn, set_id, term, definition):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flashcards (set_id, word, definition) VALUES (?, ?, ?)', (set_id, term, definition))
    conn.commit()

def get_sets(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM flashcards_sets')
    rows = cursor.fetchall()
    return {row[1]: row[0] for row in rows}

def get_flashcards(conn, set_id):
    cursor = conn.cursor()
    cursor.execute('SELECT word, definition FROM flashcards WHERE set_id = ?', (set_id,))
    return cursor.fetchall()

def delete_set(conn, set_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flashcards WHERE set_id = ?', (set_id,))
    cursor.execute('DELETE FROM flashcards_sets WHERE id = ?', (set_id,))
    conn.commit()

# Functions for UI interactions
def create_set():
    set_name = set_name_var.get()
    if set_name:
        sets = get_sets(conn)
        if set_name not in sets:
            add_set(conn, set_name)
            refresh_deck_cards()
            messagebox.showinfo('Success', f'Set "{set_name}" created.')
        else:
            messagebox.showwarning('Warning', f'Set "{set_name}" already exists.')
    else:
        messagebox.showwarning('Warning', 'Please enter a valid deck name.')
    set_name_var.set('')

def add_word():
    set_name = set_name_var.get()
    term = term_var.get()
    definition = definition_var.get()
    if set_name and term and definition:
        sets = get_sets(conn)
        set_id = sets.get(set_name) or add_set(conn, set_name)
        add_flashcard(conn, set_id, term, definition)
        term_var.set('')
        definition_var.set('')
        refresh_deck_cards()
        messagebox.showinfo('Success', f'Term "{term}" added to the deck "{set_name}".')
    else:
        messagebox.showwarning('Warning', 'Please fill in all fields.')

def refresh_deck_cards():
    # Clear existing cards
    for widget in cards_frame.winfo_children():
        widget.destroy()

    # Add cards for each deck
    sets = get_sets(conn)
    for set_name, set_id in sets.items():
        card = ttk.Frame(cards_frame, padding=10, relief='ridge', style='Card.TFrame')
        card.pack(fill='x', pady=5)

        label = ttk.Label(card, text=set_name, font=('Helvetica', 14, 'bold'))
        label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        button_load = ttk.Button(card, text='Load Deck', command=lambda s=set_id: load_deck(s))
        button_load.grid(row=0, column=1, padx=10)

        button_delete = ttk.Button(card, text='Delete Deck', command=lambda s=set_id: delete_and_refresh(s))
        button_delete.grid(row=0, column=2, padx=10)

def load_deck(set_id):
    cards = get_flashcards(conn, set_id)
    display_flashcards(cards)

def delete_and_refresh(set_id):
    delete_set(conn, set_id)
    refresh_deck_cards()

def display_flashcards(cards):
    global current_cards, card_index, card_flipped
    current_cards = cards
    card_index = 0
    card_flipped = False
    show_card()

def show_card():
    if current_cards and 0 <= card_index < len(current_cards):
        term, definition = current_cards[card_index]
        word_label.config(text=term)
        definition_label.config(text=definition if card_flipped else 'Flip to see the definition')
    else:
        word_label.config(text='No cards available')
        definition_label.config(text='')

def next_card():
    global card_index, card_flipped
    if current_cards and card_index < len(current_cards) - 1:
        card_index += 1
        card_flipped = False
        show_card()

def prev_card():
    global card_index, card_flipped
    if current_cards and card_index > 0:
        card_index -= 1
        card_flipped = False
        show_card()

def flip_card():
    global card_flipped
    card_flipped = not card_flipped
    show_card()

# Main application
if __name__ == '__main__':
    conn = sqlite3.connect('flashcards.db')
    create_tables(conn)

    root = tk.Tk()
    root.title('Synapse Flashcards')
    root.geometry('600x500')

    # Modern theme setup
    style = Style(theme='cosmo')
    style.configure('Card.TFrame', background='#f0f0f0', borderwidth=1, relief='solid')

    set_name_var = tk.StringVar()
    term_var = tk.StringVar()
    definition_var = tk.StringVar()

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create Set Tab
    create_set_frame = ttk.Frame(notebook, padding=20)
    notebook.add(create_set_frame, text='Create Deck')

    ttk.Label(create_set_frame, text='Deck Name:').pack(pady=5)
    ttk.Entry(create_set_frame, textvariable=set_name_var).pack(pady=5)

    ttk.Label(create_set_frame, text='Term:').pack(pady=5)
    ttk.Entry(create_set_frame, textvariable=term_var).pack(pady=5)

    ttk.Label(create_set_frame, text='Definition:').pack(pady=5)
    ttk.Entry(create_set_frame, textvariable=definition_var).pack(pady=5)

    ttk.Button(create_set_frame, text='Add Term', command=add_word).pack(pady=5)
    ttk.Button(create_set_frame, text='Save Deck', command=create_set).pack(pady=5)

    # Select Set Tab
    select_set_frame = ttk.Frame(notebook, padding=20)
    notebook.add(select_set_frame, text='Select Deck')

    cards_frame = ttk.Frame(select_set_frame)
    cards_frame.pack(fill='both', expand=True, pady=10)

    # Learning Mode Tab
    learning_mode_frame = ttk.Frame(notebook, padding=20)
    notebook.add(learning_mode_frame, text='Learn Cards')

    word_label = ttk.Label(learning_mode_frame, font=('Helvetica', 16, 'bold'))
    word_label.pack(pady=10)

    definition_label = ttk.Label(learning_mode_frame, font=('Helvetica', 12), foreground='blue')
    definition_label.pack(pady=5)

    button_frame = ttk.Frame(learning_mode_frame)
    button_frame.pack(pady=20)

    ttk.Button(button_frame, text='Prev', command=prev_card).pack(side='left', padx=5)
    ttk.Button(button_frame, text='Flip', command=flip_card).pack(side='left', padx=5)
    ttk.Button(button_frame, text='Next', command=next_card).pack(side='left', padx=5)

    refresh_deck_cards()
    root.mainloop()
