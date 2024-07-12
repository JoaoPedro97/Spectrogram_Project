import tkinter as tk

def on_selection(event):
    selected_option = variable.get()
    print(f'Selecionado: {selected_option}')

root = tk.Tk()
root.geometry("250x150")
root.title("Exemplo de OptionMenu")

options = ["TCP/IP", "GPIB", "USB"]
variable = tk.StringVar(root)
variable.set(options[0])  # Define o valor padrão

option_menu = tk.OptionMenu(root, variable, *options)
option_menu.config(width=20)
option_menu.pack()

variable.trace("w", on_selection)

root.mainloop()
