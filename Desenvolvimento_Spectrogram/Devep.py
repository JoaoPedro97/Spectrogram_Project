from asyncio import selector_events
from logging import root
from msilib.schema import CheckBox, ListBox
from re import match
import tkinter as tk
from tkinter import LEFT, RIGHT, TOP, Checkbutton, LabelFrame, Listbox, Menu, Toplevel, Widget, messagebox, Entry, Label, Button, Frame
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
        self.lb.itemconfig(tk.END, {'fg': 'green'})# Janela Connection

class CommandTestWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("850x550")
        self.title("Teste de Envio de Comandos")

        self.create_widgets_Commandos()

    def create_widgets_Commandos(self):
        self.container_conect = tk.LabelFrame(self, text="Comandos de preset",font = ("Arial","12","bold"))
        self.container_conect.pack(side=tk.TOP)
        
        self.Boxline_1 = tk.Frame(self.container_conect)
        self.Boxline_1.pack(side=tk.TOP)
        
        self.Boxline_2 = tk.Frame(self.container_conect)
        self.Boxline_2.pack(side=tk.TOP)
       
        self.BW_Box() #container com as entradas de RBW e VBW
        self.Sweep_box() #Container com as Entradas de Sweep
        self.Frequency_box() #Container com as entradas de Frequencia

        
    def BW_Box(self):
        # Frame BW - Set de RBW e VBW
        self.BandWidth_Contains = tk.LabelFrame(self.Boxline_1, text="BW", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.BandWidth_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # linha RBW
        self.RBW_Label = tk.Label(self.BandWidth_Contains, text="RBW", font=("Calibri", "10"))
        self.RBW_Label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.EntryRBW = tk.Entry(self.BandWidth_Contains, width=10)
        self.EntryRBW.grid(row=0, column=1, sticky="e")
        self.KHz_Label_01 = tk.Label(self.BandWidth_Contains, text="kHz", font=("Calibri", "8"))
        self.KHz_Label_01.grid(row=0, column=2, sticky="e")

        # linha VBW
        self.VBW_Label = tk.Label(self.BandWidth_Contains, text="VBW", font=("Calibri", "10"))
        self.VBW_Label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.EntryVBW = tk.Entry(self.BandWidth_Contains, width=10)
        self.EntryVBW.grid(row=1, column=1, sticky="e")
        self.KHz_Label_02 = tk.Label(self.BandWidth_Contains, text="kHz", font=("Calibri", "8"))
        self.KHz_Label_02.grid(row=1, column=2, sticky="e")

        # linha Sweep Time
        self.SweepTimeLabel = tk.Label(self.BandWidth_Contains, text="Sweep Time", font=("Calibri", "10"))
        self.SweepTimeLabel.grid(row=2, column=0, sticky="w", padx=(0, 10))
        self.EntrySweepTime = tk.Entry(self.BandWidth_Contains, width=10)
        self.EntrySweepTime.grid(row=2, column=1, sticky="e")
        self.Segundos_Sweep = tk.Label(self.BandWidth_Contains, text="Seg", font=("Calibri", "8"))
        self.Segundos_Sweep.grid(row=2, column=2, sticky="e")

        # Configurando as colunas para ajustar o alinhamento
        self.BandWidth_Contains.grid_columnconfigure(0, weight=1)
        self.BandWidth_Contains.grid_columnconfigure(1, weight=1)
        self.BandWidth_Contains.grid_columnconfigure(2, weight=1)
        
    def Sweep_box(self):
        # Frame Sweep
        self.Sweep_Contains = tk.LabelFrame(self.Boxline_1, text="Sweep", font=("Calibri", "10", "bold"), padx=25, pady=5)
        self.Sweep_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # linha 1 Sweep continuous
        self.ContinuosSweepLabel = tk.Label(self.Sweep_Contains, text="Continuous Sweep", font=("Calibri", "10"))
        self.ContinuosSweepLabel.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.Cont_Sweep_Mark = tk.Checkbutton(self.Sweep_Contains)
        self.Cont_Sweep_Mark.grid(row=0, column=1, sticky="e")

        # linha 2 Single Sweep
        self.SingleSweepLabel = tk.Label(self.Sweep_Contains, text="Single Sweep", font=("Calibri", "10"))
        self.SingleSweepLabel.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.Single_Sweep_Mark = tk.Checkbutton(self.Sweep_Contains)
        self.Single_Sweep_Mark.grid(row=1, column=1, sticky="e")

        # linha 3 Sweep cont
        self.SweepContLabel = tk.Label(self.Sweep_Contains, text="Sweep cont", font=("Calibri", "10"))
        self.SweepContLabel.grid(row=2, column=0, sticky="w", padx=(0, 10))
        self.Sweep_Cont_Entry = tk.Entry(self.Sweep_Contains, width=10)
        self.Sweep_Cont_Entry.grid(row=2, column=1, sticky="e")

        # linha 4 Single Sweep
        self.Sweep_PointLabel = tk.Label(self.Sweep_Contains, text="Single Sweep", font=("Calibri", "10"))
        self.Sweep_PointLabel.grid(row=3, column=0, sticky="w", padx=(0, 10))
        self.Sweep_Point_Entry = tk.Entry(self.Sweep_Contains, width=10)
        self.Sweep_Point_Entry.grid(row=3, column=1, sticky="e")

        # Configurando as colunas para ajustar o alinhamento
        self.Sweep_Contains.grid_columnconfigure(0, weight=1)
        self.Sweep_Contains.grid_columnconfigure(1, weight=1)
        
    def Frequency_box(self):
        # Frame Frequency - Set de CENTER, START e STOP
        self.Frequency_Contains = tk.LabelFrame(self.Boxline_1, text="FREQ", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Frequency_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # linha CENTER
        self.Center_Checkbox = tk.Checkbutton(self.Frequency_Contains)
        self.Center_Checkbox.grid(row=0, column=0, sticky="w")
        self.Center_Label = tk.Label(self.Frequency_Contains, text="CENTER", font=("Calibri", "10"))
        self.Center_Label.grid(row=0, column=1, sticky="w", padx=(0, 10))
        self.Center_Entry = tk.Entry(self.Frequency_Contains, width=10)
        self.Center_Entry.grid(row=0, column=2, sticky="e")
        self.Center_MHz_Label = tk.Label(self.Frequency_Contains, text="MHz", font=("Calibri", "8"))
        self.Center_MHz_Label.grid(row=0, column=3, sticky="e")

        # linha START
        self.Start_Checkbox = tk.Checkbutton(self.Frequency_Contains)
        self.Start_Checkbox.grid(row=1, column=0, sticky="w")
        self.Start_Label = tk.Label(self.Frequency_Contains, text="START", font=("Calibri", "10"))
        self.Start_Label.grid(row=1, column=1, sticky="w", padx=(0, 10))
        self.Start_Entry = tk.Entry(self.Frequency_Contains, width=10)
        self.Start_Entry.grid(row=1, column=2, sticky="e")
        self.Start_MHz_Label = tk.Label(self.Frequency_Contains, text="MHz", font=("Calibri", "8"))
        self.Start_MHz_Label.grid(row=1, column=3, sticky="e")

        # linha STOP
        self.Stop_Checkbox = tk.Checkbutton(self.Frequency_Contains)
        self.Stop_Checkbox.grid(row=2, column=0, sticky="w")
        self.Stop_Label = tk.Label(self.Frequency_Contains, text="STOP", font=("Calibri", "10"))
        self.Stop_Label.grid(row=2, column=1, sticky="w", padx=(0, 10))
        self.Stop_Entry = tk.Entry(self.Frequency_Contains, width=10)
        self.Stop_Entry.grid(row=2, column=2, sticky="e")
        self.Stop_MHz_Label = tk.Label(self.Frequency_Contains, text="MHz", font=("Calibri", "8"))
        self.Stop_MHz_Label.grid(row=2, column=3, sticky="e")

        # Configurando as colunas para ajustar o alinhamento
        self.Frequency_Contains.grid_columnconfigure(0, weight=1)
        self.Frequency_Contains.grid_columnconfigure(1, weight=1)
        self.Frequency_Contains.grid_columnconfigure(2, weight=1)
        self.Frequency_Contains.grid_columnconfigure(3, weight=1)
        
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
            messagebox.showerror("Error", "IP not set. Please connect to an instrument first.") # Janela de comando para teste

class SettingsWindow(tk.Toplevel):
    # variaveis

    def __init__(self, master):
        super().__init__(master)
        self.geometry("450x300")
        self.title("Configuracoes")

        self.Connect()

    def Connect(self):
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
        CommandTestWindow(self) # Janela de configuracoes

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
