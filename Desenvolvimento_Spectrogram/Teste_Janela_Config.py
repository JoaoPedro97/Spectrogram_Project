from asyncio import selector_events
from asyncio.windows_events import NULL
#from distutils.dist import command_re
from logging import root
from msilib.schema import CheckBox, ListBox
from re import match
import tkinter as tk
from tkinter import LEFT, RIGHT, SEL_FIRST, TOP, Checkbutton, LabelFrame, Listbox, Menu, Toplevel, Widget, messagebox, Entry, Label, Button, Frame
from tkinter import messagebox, scrolledtext
from RsInstrument.RsInstrument import RsInstrument
import os
from datetime import datetime
import sqlite3

# Variavel global para armazenar o IP
global_ip = ""
global_COM_Option = ["TCP/IP", "GPIB", "USB"]
global_Unidade_select = ["dBm","dBmV", "dBuV", "dBuA", "dBpW", "Volts", "Amper", "Watt"]
global_Unidade_Medida_Select = ["Hz","kHz","MHz","GHz"]
global_Unidade_Medida_Time = ["ns","ms","us","s"]

def save_log(idn, driver, visa_manufacturer, instrument_full_name):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "instrument_log.csv")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"{idn};{driver};{visa_manufacturer};{instrument_full_name};{current_time}\\n"

    with open(log_file, "a") as file:
        file.write(log_entry)
    messagebox.showinfo("Log Saved", "The log has been saved successfully.")

class ConnectionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("350x200")
        self.title("Conectar ao Instrumento")

# Funcao para inicializar o banco de dados e criar a tabela de presets
def init_db():
    conn = sqlite3.connect('presets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            settings TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chamando a funcao para inicializar o banco de dados
init_db()

# Funcoes para salvar e carregar presets
def save_preset(name, settings):
    conn = sqlite3.connect('presets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO presets (name, settings)
        VALUES (?, ?)
    ''', (name, settings))
    conn.commit()
    conn.close()

def load_preset(name):
    conn = sqlite3.connect('presets.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT settings FROM presets
        WHERE name = ?
    ''', (name,))
    settings = cursor.fetchone()
    conn.close()
    return settings[0] if settings else None

def get_preset_ids():
    conn = sqlite3.connect('presets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM presets')
    ids = cursor.fetchall()
    conn.close()
    return ids

class PresetWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x300")
        self.title("Salvar/Carregar Preset")

        self.name_label = tk.Label(self, text="Nome do Preset")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.save_button = tk.Button(self, text="Salvar Preset", command=self.save_preset)
        self.save_button.pack()

        self.load_button = tk.Button(self, text="Carregar Preset", command=self.load_preset)
        self.load_button.pack()

        self.list_ids_button = tk.Button(self, text="Listar IDs", command=self.list_ids)
        self.list_ids_button.pack()

        self.ids_listbox = tk.Listbox(self)
        self.ids_listbox.pack()

        self.settings_text = tk.Text(self)
        self.settings_text.pack()

    def save_preset(self):
        name = self.name_entry.get()
        settings = self.settings_text.get("1.0", tk.END)
        save_preset(name, settings)
        messagebox.showinfo("Preset Salvo", "O preset foi salvo com sucesso.")

    def load_preset(self):
        name = self.name_entry.get()
        settings = load_preset(name)
        if settings:
            self.settings_text.delete("1.0", tk.END)
            self.settings_text.insert(tk.END, settings)
            messagebox.showinfo("Preset Carregado", "O preset foi carregado com sucesso.")
        else:
            messagebox.showerror("Erro", "Preset nao encontrado.")

    def list_ids(self):
        ids = get_preset_ids()
        self.ids_listbox.delete(0, tk.END)
        for id, name in ids:
            self.ids_listbox.insert(tk.END, f"{id}: {name}")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacao Principal")
        self.geometry("800x600")

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)

        self.preset_menu = tk.Menu(self.edit_menu, tearoff=0)
        self.edit_menu.add_cascade(label="Preset", menu=self.preset_menu)
        self.preset_menu.add_command(label="Novo", command=self.open_preset_window)

    def open_preset_window(self):
        PresetWindow(self)

# Iniciando a aplicacao
if __name__ == "__main__":
    app = Application()
    app.mainloop()