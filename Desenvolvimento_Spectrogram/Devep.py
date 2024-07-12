from asyncio import selector_events
from logging import root
from msilib.schema import ListBox
from re import match
import tkinter as tk
from tkinter import LEFT, RIGHT, TOP, LabelFrame, Listbox, Menu, Toplevel, messagebox, Entry, Label, Button, Frame
from typing import Text
from RsInstrument.RsInstrument import RsInstrument
import os
from datetime import datetime


# Variável global para armazenar o IP
global_ip = ""
global_COM_Option = ["TCP/IP", "GPIB", "USB"]


def save_log(idn, driver, visa_manufacturer, instrument_full_name):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "instrument_log.csv")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"{idn};{driver};{visa_manufacturer};{instrument_full_name};{current_time}\n"

    with open(log_file, "a") as file:
        file.write(log_entry)
    messagebox.showinfo("Log Saved", "The log has been saved successfully.")

class ConnectionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("350x200")
        self.title("Conectar ao Instrumento")

        self.create_widgets()

    def create_widgets(self):
        self.Container_1 = tk.LabelFrame(self, text="Instrument Connection", padx=10, pady=10)
        self.Container_1.pack(side=tk.TOP)

        self.FirthPackIP = tk.Frame(self.Container_1)
        self.FirthPackIP.pack(side=tk.TOP)

        self.LABIP = tk.Label(self.FirthPackIP, text="IP", font=("Calibri", "12", "bold"))
        self.LABIP.pack(side=tk.LEFT)

        self.EntradaIP = tk.Entry(self.FirthPackIP, font=("Arial", "10"), width=15)
        self.EntradaIP.pack(side=tk.LEFT)

        self.ConnectingButton = tk.Button(self.FirthPackIP, text="Connect", command=self.authenticate, font=("Calibri", "10"), width=15)
        self.ConnectingButton.pack(side=tk.RIGHT)

        self.Container_2 = tk.LabelFrame(self.Container_1, text="Dados do equipamento", pady=5)
        self.Container_2.pack(side=tk.TOP)

        self.lb = tk.Listbox(self.Container_2, width=45, height=6)
        self.lb.pack(side=tk.TOP, expand=True)

        self.Container_3 = tk.Frame(self.Container_1, padx=10, pady=10)
        self.Container_3.pack()

    def authenticate(self):
        global global_ip
        global_ip = self.EntradaIP.get()
        try:
            self.resource_string_1 = f'TCPIP::{global_ip}::INSTR'
            self.instr = RsInstrument(self.resource_string_1, True, False)
            idn = self.instr.query_str('*IDN?')
            driver = self.instr.driver_version
            visa_manufacturer = self.instr.visa_manufacturer
            instrument_full_name = self.instr.full_instrument_model_name

            info = f"Name: {idn}\nRsInstrument Driver Version: {driver}\nVisa Manufacturer: {visa_manufacturer}\nInstrument Full Name: {instrument_full_name}"
            messagebox.showinfo("Instrument informations", info)
        except Exception as e:
            messagebox.showerror("Error", f"Connections Fail!\n{e}")
            self.lb.delete(0, tk.END)
            return
        else:
            self.lb.delete(0, tk.END)
            self.info_instrument(idn, driver, visa_manufacturer, instrument_full_name)
            save_log(idn, driver, visa_manufacturer, instrument_full_name)

    def info_instrument(self, idn, driver, visa_manufacturer, instrument_full_name):
        self.lb.insert(tk.END, 'Name: ' + idn)
        self.lb.insert(tk.END, 'RsInstrument Driver Version: ' + driver)
        self.lb.insert(tk.END, 'Visa Manufacturer: ' + visa_manufacturer)
        self.lb.insert(tk.END, 'Instrument full name: ' + instrument_full_name)
        self.lb.insert(tk.END, 'Instrument Installed Options: ' + ",".join(self.instr.instrument_options))
        self.lb.insert(tk.END, "Connection Success")
        self.lb.itemconfig(tk.END, {'fg': 'green'})

class CommandTestWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("350x200")
        self.title("Teste de Envio de Comandos")

        self.create_widgets()

    def create_widgets(self):
        self.label_rbw = tk.Label(self, text="RBW (kHz):")
        self.label_rbw.grid(row=0, column=0, padx=10, pady=10)
        self.entry_rbw = tk.Entry(self)
        self.entry_rbw.grid(row=0, column=1, padx=10, pady=10)

        self.label_vbw = tk.Label(self, text="VBW (kHz):")
        self.label_vbw.grid(row=1, column=0, padx=10, pady=10)
        self.entry_vbw = tk.Entry(self)
        self.entry_vbw.grid(row=1, column=1, padx=10, pady=10)

        self.button_reset = tk.Button(self, text="RESET", command=self.reset_instrument)
        self.button_reset.grid(row=2, column=0, padx=10, pady=10)

        self.button_max_hold = tk.Button(self, text="Trace: Max Hold", command=self.set_max_hold)
        self.button_max_hold.grid(row=2, column=1, padx=10, pady=10)

    def reset_instrument(self):
        if global_ip:
            try:
                instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
                instr.write_str("*RST")
                messagebox.showinfo("Success", "Instrument reset successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset instrument.\n{e}")
        else:
            messagebox.showerror("Error", "IP not set. Please connect to an instrument first.")

    def set_max_hold(self):
        if global_ip:
            try:
                instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
                rbw = self.entry_rbw.get()
                vbw = self.entry_vbw.get()
                instr.write_str(f"BAND {rbw}kHz")
                instr.write_str(f"BAND:VID {vbw}kHz")
                instr.write_str("DISP:WIND:TRAC:MODE MAXH")
                messagebox.showinfo("Success", "Max hold set successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set max hold.\n{e}")
        else:
            messagebox.showerror("Error", "IP not set. Please connect to an instrument first.")

class SettingsWindow(tk.Toplevel):
    # variaveis

    def __init__(self, master):
        super().__init__(master)
        self.geometry("450x300")
        self.title("Configuracoes")

        self.Conect()
        #self.create_widgets()

    def Conect(self):
        #Espaco de conexao-Menu
        self.Select_COM = tk.StringVar(self)
        self.Select_COM.set(global_COM_Option[0]) #Define TCP/IP como padrao (no futuro, mudar para o que esta setado pelo usuário)
        self.container_conect = tk.LabelFrame(self, text="Conecxoes/protocolo de comunicacao", padx=25, pady=10)
        self.container_conect.pack(side=tk.TOP)
        
        self.contant_Conection = tk.Frame(self.container_conect)
        self.contant_Conection.pack(side=tk.TOP)
        
        self.LabelTipoCom = tk.Label(self.contant_Conection, text="Tipo de conexao", font=("Calibri", "10"))
        self.LabelTipoCom.pack(side=tk.LEFT)
        
        self.blankFrame_1 = tk.Frame(self.contant_Conection)
        self.blankFrame_1.config(width=250)
        self.blankFrame_1.pack(side=tk.RIGHT)

        self.option_menu = tk.OptionMenu(self.container_conect,self.Select_COM,*global_COM_Option)
        self.option_menu.config(width = 20)
        self.option_menu.pack(side=tk.LEFT)
        
        self.blankFrame_2 = tk.Frame(self.container_conect)
        self.blankFrame_2.config(width=25)
        self.blankFrame_2.pack(side=tk.BOTTOM)

        self.AplicarButton = tk.Button(self.container_conect,text="Aplicar",command=self.MSG, font=("Calibri", "10"), width=15)
        self.AplicarButton.pack(side=tk.RIGHT)

        #Espaco de teste COM
        self.container_TEST = tk.LabelFrame(self, text="Teste COM", padx=25, pady=10)
        self.container_TEST.pack(side=tk.TOP)
        
        self.Espaco_1 = tk.Frame(self.container_TEST)
        self.Espaco_1.pack(side=tk.TOP)

        self.Texto_Inf = tk.Label(self.Espaco_1,text="Selecao para testes de envio de comando:",font=("Calibri", "10"))
        self.Texto_Inf.pack(side=tk.LEFT)
        
        self.blankFrame_null_1 = tk.Frame(self.Espaco_1)
        self.blankFrame_null_1.config(width=110)
        self.blankFrame_null_1.config(height=25)
        self.blankFrame_null_1.pack(side=tk.BOTTOM)

        self.EnvioPresetButton = tk.Button(self.container_TEST,text="Envio de preset",command=self.open_command_test_window, font=("Calibri", "10"), width=15)
        self.EnvioPresetButton.pack(side=tk.LEFT)
        
        self.blankFrame_null = tk.Frame(self.container_TEST)
        self.blankFrame_null.config(width=230)
        self.blankFrame_null.pack(side=tk.BOTTOM)

        self.AplicarButton = tk.Button(self.container_TEST,text="Envio de comandos",command=self.MSG, font=("Calibri", "10"), width=15)
        self.AplicarButton.pack(side=tk.RIGHT)

        #Espaco de config dos containers
        self.container_Config = tk.LabelFrame(self, text="Configuracao containers", padx=165, pady=10)
        self.container_Config.pack(side=tk.TOP)
        
        self.Espaco_2 = tk.Frame(self.container_Config)
        self.Espaco_2.pack(side=tk.TOP)
        
        self.InfoLabel = tk.Label(self.container_Config,text="Em breve...")
        self.InfoLabel.pack(side=tk.LEFT)
        
    def MSG(self): #mensagem para oprimeiro botao: Este codigo e temporario
        Option_select = self.Select_COM.get() 
        messagebox.showinfo("Success", f"Program config to {Option_select} for connect")
           
    def create_widgets(self):
        self.test_command_button = tk.Button(self, text="Teste de Envio de Comandos", command=self.open_command_test_window)
        self.test_command_button.pack(pady=20)

    def open_command_test_window(self):
        CommandTestWindow(self)

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spectrogram Alfa")
        self.master.geometry("500x400")

        self.create_menu()

    def create_menu(self):
        menubar = Menu(self.master)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Novo")
        file_menu.add_command(label="Abrir")
        file_menu.add_command(label="Conectar", command=self.open_connection_window)
        file_menu.add_command(label="Arquivo")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.master.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Configuracoes", command=self.open_settings_window)
        preset_menu = Menu(edit_menu, tearoff=0)
        preset_menu.add_command(label="Novo")
        preset_menu.add_command(label="Editar")
        preset_menu.add_command(label="Excluir")
        edit_menu.add_cascade(label="Preset", menu=preset_menu)
        edit_menu.add_command(label="Logs")
        menubar.add_cascade(label="Editar", menu=edit_menu)

        self.master.config(menu=menubar)

    def open_connection_window(self):
        ConnectionWindow(self.master)

    def open_settings_window(self):
        SettingsWindow(self.master)

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
