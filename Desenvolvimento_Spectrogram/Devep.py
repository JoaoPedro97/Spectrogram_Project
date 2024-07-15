from asyncio import selector_events
from asyncio.windows_events import NULL
from distutils.dist import command_re
from logging import root
from msilib.schema import CheckBox, ListBox
from re import match
import tkinter as tk
from tkinter import LEFT, RIGHT, SEL_FIRST, TOP, Checkbutton, LabelFrame, Listbox, Menu, Toplevel, Widget, messagebox, Entry, Label, Button, Frame
from tkinter import messagebox, scrolledtext
from RsInstrument.RsInstrument import RsInstrument
import os
from datetime import datetime


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
        self.geometry("900x550")
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
        self.Span_box() #Container com as entradas de SPAN
        self.Amp_box() #Container com as entradas de AMP
        self.Trace_box() #Container com as entradas TRACE
        
        self.container_Send_Command = tk.LabelFrame(self, text="Envio do commando",font = ("Arial","12","bold"))
        self.container_Send_Command.pack(side=tk.TOP)  
        
        self.Boxline_1A = tk.Frame(self.container_Send_Command)
        self.Boxline_1A.pack(side=tk.TOP)

        self.buttom_Send() #Botao de envio dos comandos
        self.buttom_Reset() #Botao de Reset
        
        self.Boxline_2A = tk.Frame(self.container_Send_Command)
        self.Boxline_2A.pack(side=tk.TOP)
        
        


    def BW_Box(self):
        self.Pre_Select_UnitRBW = tk.StringVar(self)
        self.Pre_Select_UnitRBW.set(global_Unidade_Medida_Select[1])        
        self.Pre_Select_UnitVBW = tk.StringVar(self)
        self.Pre_Select_UnitVBW.set(global_Unidade_Medida_Select[1])
        self.Pre_Select_UnitSeg = tk.StringVar(self)
        self.Pre_Select_UnitSeg.set(global_Unidade_Medida_Time[1])
        # Frame BW - Set de RBW e VBW
        self.BandWidth_Contains = tk.LabelFrame(self.Boxline_1, text="BW", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.BandWidth_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # linha RBW
        self.RBW_Label = tk.Label(self.BandWidth_Contains, text="RBW", font=("Calibri", "10"))
        self.RBW_Label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.EntryRBW = tk.Entry(self.BandWidth_Contains, width=10)
        self.EntryRBW.grid(row=0, column=1, sticky="e")
        self.option_UnitRBW = tk.OptionMenu(self.BandWidth_Contains,self.Pre_Select_UnitRBW,*global_Unidade_Medida_Select)
        self.option_UnitRBW.grid(row=0, column=2, sticky="w", padx=(0, 10))
        
        # linha VBW
        self.VBW_Label = tk.Label(self.BandWidth_Contains, text="VBW", font=("Calibri", "10"))
        self.VBW_Label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.EntryVBW = tk.Entry(self.BandWidth_Contains, width=10)
        self.EntryVBW.grid(row=1, column=1, sticky="e")
        self.option_UnitVBW = tk.OptionMenu(self.BandWidth_Contains,self.Pre_Select_UnitVBW,*global_Unidade_Medida_Select)
        self.option_UnitVBW.grid(row=1, column=2, sticky="w", padx=(0, 10))

        # linha Sweep Time
        self.SweepTimeLabel = tk.Label(self.BandWidth_Contains, text="Sweep Time", font=("Calibri", "10"))
        self.SweepTimeLabel.grid(row=2, column=0, sticky="w", padx=(0, 10))
        self.EntrySweepTime = tk.Entry(self.BandWidth_Contains, width=10)
        self.EntrySweepTime.grid(row=2, column=1, sticky="e")
        self.option_UnitSegundos = tk.OptionMenu(self.BandWidth_Contains,self.Pre_Select_UnitSeg,*global_Unidade_Medida_Time)
        self.option_UnitSegundos.grid(row=2, column=2, sticky="w", padx=(0, 10))

        # Configurando as colunas para ajustar o alinhamento
        self.BandWidth_Contains.grid_columnconfigure(0, weight=1)
        self.BandWidth_Contains.grid_columnconfigure(1, weight=1)
        self.BandWidth_Contains.grid_columnconfigure(2, weight=1)
        
    def Sweep_box(self):
        # Frame Sweep
        self.Sweep_Contains = tk.LabelFrame(self.Boxline_1, text="Sweep", font=("Calibri", "10", "bold"), padx=25, pady=5)
        self.Sweep_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # Variavel para armazenar a seleção do Sweep
        self.sweep_var = tk.StringVar(value="Continuous Sweep")

        # linha 1 Sweep continuous
        self.ContinuosSweepLabel = tk.Label(self.Sweep_Contains, text="Continuous Sweep", font=("Calibri", "10"))
        self.ContinuosSweepLabel.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.Cont_Sweep_Radiobutton = tk.Radiobutton(self.Sweep_Contains, variable=self.sweep_var, value="Continuous Sweep")
        self.Cont_Sweep_Radiobutton.grid(row=0, column=1, sticky="e")

        # linha 2 Single Sweep
        self.SingleSweepLabel = tk.Label(self.Sweep_Contains, text="Single Sweep", font=("Calibri", "10"))
        self.SingleSweepLabel.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.Single_Sweep_Radiobutton = tk.Radiobutton(self.Sweep_Contains, variable=self.sweep_var, value="Single Sweep")
        self.Single_Sweep_Radiobutton.grid(row=1, column=1, sticky="e")

        # linha 3 Sweep cont
        self.SweepContLabel = tk.Label(self.Sweep_Contains, text="Sweep cont", font=("Calibri", "10"))
        self.SweepContLabel.grid(row=2, column=0, sticky="w", padx=(0, 10))
        self.Sweep_Cont_Entry = tk.Entry(self.Sweep_Contains, width=10)
        self.Sweep_Cont_Entry.grid(row=2, column=1, sticky="e")

        # linha 4 Single Sweep
        self.Sweep_Point_Label = tk.Label(self.Sweep_Contains, text="Sweep Point", font=("Calibri", "10"))
        self.Sweep_Point_Label.grid(row=3, column=0, sticky="w", padx=(0, 10))
        self.Sweep_Point_Entry = tk.Entry(self.Sweep_Contains, width=10)
        self.Sweep_Point_Entry.grid(row=3, column=1, sticky="e")

        # Configurando as colunas para ajustar o alinhamento
        self.Sweep_Contains.grid_columnconfigure(0, weight=1)
        self.Sweep_Contains.grid_columnconfigure(1, weight=1)
        
    def Frequency_box(self):
        self.Pre_Select_UnitCenter = tk.StringVar(self)
        self.Pre_Select_UnitCenter.set(global_Unidade_Medida_Select[1])        
        self.Pre_Select_UnitSTART = tk.StringVar(self)
        self.Pre_Select_UnitSTART.set(global_Unidade_Medida_Select[1])  
        self.Pre_Select_UnitSTOP = tk.StringVar(self)
        self.Pre_Select_UnitSTOP.set(global_Unidade_Medida_Select[1])        
        # Frame Frequency - Set de CENTER, START e STOP
        self.Frequency_Contains = tk.LabelFrame(self.Boxline_1, text="FREQ", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Frequency_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # linha CENTER
        self.Center_Label = tk.Label(self.Frequency_Contains, text="CENTER", font=("Calibri", "10"))
        self.Center_Label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.Center_Entry = tk.Entry(self.Frequency_Contains, width=10)
        self.Center_Entry.grid(row=0, column=1, sticky="e")
        self.option_UnitCENTER = tk.OptionMenu(self.Frequency_Contains,self.Pre_Select_UnitCenter,*global_Unidade_Medida_Select)
        self.option_UnitCENTER.grid(row=0, column=2, sticky="w", padx=(0, 10))

        # linha START
        self.Start_Label = tk.Label(self.Frequency_Contains, text="START", font=("Calibri", "10"))
        self.Start_Label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.Start_Entry = tk.Entry(self.Frequency_Contains, width=10)
        self.Start_Entry.grid(row=1, column=1, sticky="e")
        self.option_UnitSTART = tk.OptionMenu(self.Frequency_Contains,self.Pre_Select_UnitSTART,*global_Unidade_Medida_Select)
        self.option_UnitSTART.grid(row=1, column=2, sticky="w", padx=(0, 10))

        # linha STOP
        self.Stop_Label = tk.Label(self.Frequency_Contains, text="STOP", font=("Calibri", "10"))
        self.Stop_Label.grid(row=2, column=0, sticky="w", padx=(0, 10))
        self.Stop_Entry = tk.Entry(self.Frequency_Contains, width=10)
        self.Stop_Entry.grid(row=2, column=1, sticky="e")
        self.option_UnitSTOP = tk.OptionMenu(self.Frequency_Contains,self.Pre_Select_UnitSTOP,*global_Unidade_Medida_Select)
        self.option_UnitSTOP.grid(row=2, column=2, sticky="w", padx=(0, 10))

        # Configurando as colunas para ajustar o alinhamento
        self.Frequency_Contains.grid_columnconfigure(0, weight=1)
        self.Frequency_Contains.grid_columnconfigure(1, weight=1)
        self.Frequency_Contains.grid_columnconfigure(2, weight=1)
        self.Frequency_Contains.grid_columnconfigure(3, weight=1)
        
    def Span_box(self):
        self.Pre_Select_UnitSPAN = tk.StringVar(self)
        self.Pre_Select_UnitSPAN.set(global_Unidade_Medida_Select[1])        
        # Frame Span - Set de Manual, Zero e Full Span
        self.Span_Contains = tk.LabelFrame(self.Boxline_2, text="SPAN", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Span_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # Variavel para armazenar a seleção do Span
        self.span_var = tk.StringVar(value="Span Manual")

        # linha Span Manual
        self.Span_Radiobutton = tk.Radiobutton(self.Span_Contains, variable=self.span_var, value="Span Manual")
        self.Span_Radiobutton.grid(row=0, column=0, sticky="e")        
        self.Span_Label = tk.Label(self.Span_Contains, text="Span Manual", font=("Calibri", "10"))
        self.Span_Label.grid(row=0, column=1, sticky="w", padx=(0, 10))
        self.Span_Entry = tk.Entry(self.Span_Contains, width=10)
        self.Span_Entry.grid(row=0, column=2, sticky="e")
        self.option_UnitSPAN = tk.OptionMenu(self.Span_Contains,self.Pre_Select_UnitSPAN,*global_Unidade_Medida_Select)
        self.option_UnitSPAN.grid(row=0, column=3, sticky="w", padx=(0, 10))

        
        # linha Zero Span
        self.Zero_Radiobutton = tk.Radiobutton(self.Span_Contains, variable=self.span_var, value="ZERO SPAN")
        self.Zero_Radiobutton.grid(row=1, column=0, sticky="e")        
        self.Zero_Label = tk.Label(self.Span_Contains, text="ZERO SPAN", font=("Calibri", "10"))
        self.Zero_Label.grid(row=1, column=1, sticky="w", padx=(0, 10))

        # linha Full Span
        self.Full_Radiobutton = tk.Radiobutton(self.Span_Contains, variable=self.span_var, value="FULL SPAN")
        self.Full_Radiobutton.grid(row=2, column=0, sticky="e")        
        self.Full_Label = tk.Label(self.Span_Contains, text="FULL SPAN", font=("Calibri", "10"))
        self.Full_Label.grid(row=2, column=1, sticky="w", padx=(0, 10))

        self.AUTO_Radiobutton = tk.Radiobutton(self.Span_Contains, variable=self.span_var, value="AUTO SPAN")
        self.AUTO_Radiobutton.grid(row=3, column=0, sticky="e")        
        self.AUTO_Label = tk.Label(self.Span_Contains, text="AUTO SPAN", font=("Calibri", "10"))
        self.AUTO_Label.grid(row=3, column=1, sticky="w", padx=(0, 10))

        # Configurando as colunas para ajustar o alinhamento
        self.Span_Contains.grid_columnconfigure(0, weight=1)
        self.Span_Contains.grid_columnconfigure(1, weight=1)
        self.Span_Contains.grid_columnconfigure(2, weight=1)
        self.Span_Contains.grid_columnconfigure(3, weight=1)        

    def Amp_box(self):
        self.check_Range = tk.IntVar()
        self.check_Att = tk.IntVar()

        self.Pre_Select_Unit = tk.StringVar(self)
        self.Pre_Select_Unit.set(global_Unidade_select[0])
        # Frame Amp - Set de Amplitude e referencia de amplitude
        self.Amp_Contains = tk.LabelFrame(self.Boxline_2, text="AMP", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Amp_Contains.pack(side=tk.LEFT, padx=10, pady=10)        

        # linha Reference Level
        self.Ref_Level_Label = tk.Label(self.Amp_Contains, text="Ref level", font=("Calibri", "10"))
        self.Ref_Level_Label.grid(row=0, column=1, sticky="w", padx=(0, 10))
        self.Ref_Level_Entry = tk.Entry(self.Amp_Contains, width=10)
        self.Ref_Level_Entry.grid(row=0, column=2, sticky="e")
        self.Ref_Level_Label = tk.Label(self.Amp_Contains, text="dB", font=("Calibri", "8"))
        self.Ref_Level_Label.grid(row=0, column=3, sticky="e")

        #linha Log 100
        self.Range_Label = tk.Label(self.Amp_Contains, text="Range Log 100", font=("Calibri", "10"))
        self.Range_Label.grid(row=1, column=1, sticky="w", padx=(0, 10))
        self.Range_Checkbox = tk.Checkbutton(self.Amp_Contains,variable=self.check_Range)
        self.Range_Checkbox.grid(row=1, column=2, sticky="e")
        
        #linha Unit
        self.Unit_Label = tk.Label(self.Amp_Contains, text="Unit", font=("Calibri", "10"))
        self.Unit_Label.grid(row=2, column=1, sticky="w", padx=(0, 10))
        self.option_Unit = tk.OptionMenu(self.Amp_Contains,self.Pre_Select_Unit,*global_Unidade_select)
        self.option_Unit.grid(row=2, column=2, sticky="w", padx=(0, 10))

        #linha Ref Att   
        self.Ref_Att_Label = tk.Label(self.Amp_Contains, text="Ref Att",font=("Calibri", "10"))
        self.Ref_Att_Label.grid(row=3, column=1, sticky="w", padx=(0, 10))
        self.Ref_Att_Entry = tk.Entry(self.Amp_Contains, width=10)
        self.Ref_Att_Entry.grid(row=3, column=2, sticky="e", padx=(0, 10))
        self.Ref_Att_Label_Unit = tk.Label(self.Amp_Contains, text="dB",font=("Calibri", "10"))
        self.Ref_Att_Label_Unit.grid(row=3, column=3, sticky="w", padx=(0, 10))
        self.Ref_Att_Checkbutton = tk.Checkbutton(self.Amp_Contains,variable=self.check_Att)
        self.Ref_Att_Checkbutton.grid(row=3, column=4, sticky="e")
        
    def Trace_box(self):
        self.Trace_Contains = tk.LabelFrame(self.Boxline_2, text="TRACE", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Trace_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        # Variable to hold the selected value
        self.trace_var = tk.StringVar(value="Clear/Write")

        # Clear/Write
        self.Clear_Label = tk.Label(self.Trace_Contains, text="Clear/Write", font=("Calibri", "10"))
        self.Clear_Label.grid(row=1, column=1, sticky="w", padx=(0, 10))
        self.Clear_Radiobutton = tk.Radiobutton(self.Trace_Contains, variable=self.trace_var, value="Clear/Write")
        self.Clear_Radiobutton.grid(row=1, column=2, sticky="e")

        # Max Hold
        self.Max_hold_Label = tk.Label(self.Trace_Contains, text="Max Hold", font=("Calibri", "10"))
        self.Max_hold_Label.grid(row=2, column=1, sticky="w", padx=(0, 10))
        self.Max_hold_Radiobutton = tk.Radiobutton(self.Trace_Contains, variable=self.trace_var, value="Max Hold")
        self.Max_hold_Radiobutton.grid(row=2, column=2, sticky="e")

        # AVG
        self.AVG_Label = tk.Label(self.Trace_Contains, text="AVG", font=("Calibri", "10"))
        self.AVG_Label.grid(row=3, column=1, sticky="w", padx=(0, 10))
        self.AVG_Radiobutton = tk.Radiobutton(self.Trace_Contains, variable=self.trace_var, value="AVG")
        self.AVG_Radiobutton.grid(row=3, column=2, sticky="e")

        # View
        self.View_Label = tk.Label(self.Trace_Contains, text="View", font=("Calibri", "10"))
        self.View_Label.grid(row=4, column=1, sticky="w", padx=(0, 10))
        self.View_Radiobutton = tk.Radiobutton(self.Trace_Contains, variable=self.trace_var, value="View")
        self.View_Radiobutton.grid(row=4, column=2, sticky="e")

        # Blank
        self.Blank_Label = tk.Label(self.Trace_Contains, text="Blank", font=("Calibri", "10"))
        self.Blank_Label.grid(row=5, column=1, sticky="w", padx=(0, 10))
        self.Blank_Radiobutton = tk.Radiobutton(self.Trace_Contains, variable=self.trace_var, value="Blank")
        self.Blank_Radiobutton.grid(row=5, column=2, sticky="e")
        
    def buttom_Send(self):
        self.buttom_Contains = tk.LabelFrame(self.Boxline_1A, text="Botao de envio dos comandos", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.buttom_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        self.buttom_Send = tk.Button(self.buttom_Contains,text="Enviar", command=self.set_command)
        self.buttom_Send.grid(row = 0, column = 2, padx=(0, 10))

    def buttom_Reset(self):
        self.buttom_Contains = tk.LabelFrame(self.Boxline_1A, text="Botao de reset do analisador", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.buttom_Contains.pack(side=tk.LEFT, padx=10, pady=10)

        self.buttom_Reset = tk.Button(self.buttom_Contains,text="RESET", command=self.reset_instrument)
        self.buttom_Reset.grid(row = 0, column = 2, padx=(0, 10))        
        
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

    def set_command(self):        
        if global_ip:
            try:
                #BW Variaveis
                rbw = self.EntryRBW.get()
                vbw = self.EntryVBW.get()
                SWTime = self.EntrySweepTime.get()
                URBW = self.Pre_Select_UnitRBW.get()
                UVBW = self.Pre_Select_UnitVBW.get()
                SweepTime = self.Pre_Select_UnitSeg.get()
                #Sweep - Variaveis
                ContSweep = self.sweep_var.get() #pode ser Continuous ou Single
                SweepCONT = self.Sweep_Cont_Entry.get()
                SweepPoint = self.Sweep_Point_Entry.get()
                #Freq - Variaveis
                Central = self.Center_Entry.get() 
                Inicial = self.Start_Entry.get()
                Final = self.Stop_Entry.get()
                UCENTER = self.Pre_Select_UnitCenter.get()
                USTART = self.Pre_Select_UnitSTART.get()
                USTOP = self.Pre_Select_UnitSTOP.get()
                ##SPAN - Variaveis
                DotSPAN = self.span_var.get()
                SpanManual = self.Span_Entry.get()
                SpanUnidade = self.Pre_Select_UnitSPAN.get()
                #AMP - Variaveis
                RefLevel = self.Ref_Level_Entry.get()
                RangeLog = self.check_Range.get()
                Unidade = self.Pre_Select_Unit.get()
                Att_Bool = self.check_Att.get()
                Att = self.Ref_Att_Entry.get()
                #Trace - Variavei
                TRACE = self.trace_var.get()
                
                self.bw_Command(rbw,vbw,URBW,UVBW,SweepTime,SWTime)
                self.Sweep_Command(ContSweep,SweepCONT,SweepPoint)
                self.FREQ_Command(Central,Inicial,Final,UCENTER,USTART,USTOP)
                self.SPAN_Command(DotSPAN,SpanManual,SpanUnidade)
                self.AMP_Command(RefLevel,RangeLog,Unidade,Att_Bool,Att)
                self.Trace_Command(TRACE)

                messagebox.showinfo("Success", "Preset are set successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set.\n{e}")
        else:
            messagebox.showerror("Error", "IP not set. Please connect to an instrument first.") # Janela de comando para teste

    def bw_Command(self,rbw,vbw,URBW,UVBW,SweepTime,SWTime): 
        instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
        if rbw != "":
            instr.write_str(f"BAND {rbw} {URBW}")
        else:
            pass
        if vbw != "":
            instr.write_str(f"BAND:VID {vbw} {UVBW}")
        else:
            pass
        if SWTime != "":
            instr.write_str(f"SWE:TIME {SWTime}{SweepTime}")
        else:
            pass
        
    def Sweep_Command(self,ContSweep,SweepCONT,SweepPoint):
        instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
        if SweepCONT !="":
            instr.write_str(f"SENS:SWE:COUN {SweepCONT}")
        else:
            pass
        if SweepPoint !="":
            instr.write_str(f"SENS:SWE:POIN {SweepPoint}")
        else:
            pass
        if ContSweep == "Continuous Sweep":
            instr.write_str(f"INIT:CONT ON")
        else:
            instr.write_str(f"INIT:CONT OFF; :INIT")
       
    def FREQ_Command(self,Central,Inicial,Final,UCENTER,USTART,USTOP):
        instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
        if Central != "":
            instr.write_str(f"FREQ:CENT {Central}{UCENTER}")
        else:
            pass       
        if Inicial !="":
            instr.write_str(f"FREQ:STAR {Inicial}{USTART}")
        else:
            pass
        if Final !="":
            instr.write_str(f"FREQ:STOP {Final}{USTOP}")
        else:
            pass
        
    def SPAN_Command(self,DotSPAN,SpanManual,SpanUnidade):
        instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
        if DotSPAN == "Span Manual":
            if SpanManual != "":
                instr.write_str(f"FREQ:SPAN {SpanManual}{SpanUnidade}")
            else:
                instr.write_str(f"FREQ:SPAN 100kHz")
        else:
            if DotSPAN == "ZERO SPAN":
                instr.write_str(f"FREQ:SPAN 0Hz")
            else:
                pass
            if DotSPAN == "FULL SPAN":
                instr.write_str(f"FREQ:SPAN:FULL")
            else:
                pass
            if DotSPAN == "AUTO SPAN":
                pass #SENS:FREQ:SPAN:AUTO
            else:
                pass
            
    def AMP_Command(self,RefLevel,RangeLog,Unidade,Att_Bool,Att):
        instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
        if RefLevel != "":
            instr.write_str(f"DISP:WIND:TRAC:Y:RLEV {RefLevel}dBm")
        else:
            pass
        if RangeLog:
            instr.write_str(f"DISP:WIND:TRAC:Y:SCAL:RLEV 100DB")
        else:
            pass
        instr.write_str(f"UNIT:POW {Unidade}")
        if Att_Bool:
            instr.write_str(f"INP:ATT {Att}DB")
        else:
            pass
        
    def Trace_Command(self,TRACE):
        instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
        if TRACE == "Clear/Write":
            instr.write_str(f"DISP:WIND:TRAC:MODE WRIT")
        else:
            if TRACE == "Max Hold":
                instr.write_str(f"DISP:WIND:TRAC:MODE MAXH")
            else:
                if TRACE == "AVG":
                    instr.write_str(f"DISP:WIND:TRAC:MODE AVER")
                else:
                    if TRACE == "View":
                        instr.write_str(f"DISP:WIND:TRAC:MODE VIEW")
                    else:
                        if TRACE == "Blank":
                            instr.write_str(f"DISP:WIND:TRAC:MODE BLAN")
                        else:
                            pass
                             
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
        self.Select_COM.set(global_COM_Option[0]) #Define TCP/IP como padrao (no futuro, mudar para o que esta setado pelo usuario)
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

        self.AplicarButton = tk.Button(self.container_TEST,text="Envio de comandos",command=self.open_SendCommandsWindows, font=("Calibri", "10"), width=15)
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
        
    def open_SendCommandsWindows(self):
        SendCommandsWindows(self)

class SendCommandsWindows(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Configuracao do Analisador de Espectro")
        
        # Lista de comandos que não esperam resposta
        self.comandos_sem_resposta = ["*RST?"]  # Adicione outros comandos conforme necessario

        # Frame principal
        self.frame_principal = tk.LabelFrame(self, text="Comandos para teste", font=("Calibri", 10, "bold"), padx=25, pady=10)
        self.frame_principal.pack(padx=10, pady=10)

        # Label e Entry para comandos
        self.comando_label = tk.Label(self.frame_principal, text="Comandos", font=("Calibri", 10))
        self.comando_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.comando_entry = tk.Entry(self.frame_principal, width=40)
        self.comando_entry.grid(row=0, column=1, sticky="e")
        self.comando_entry.bind("<Return>", self.enviar_comando)  # Bind para tecla Enter

        # Botão de enviar
        self.enviar_button = tk.Button(self.frame_principal, text="Enviar", command=self.enviar_comando)
        self.enviar_button.grid(row=0, column=2, padx=(10, 0))

        # Caixa de texto para o log
        self.log_text = scrolledtext.ScrolledText(self.frame_principal, width=60, height=15, wrap=tk.WORD)
        self.log_text.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        # Configurar colunas para alinhamento
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(2, weight=1)

    def enviar_comando(self, event=None):
        if global_ip:
            try:
                instr = RsInstrument(f'TCPIP::{global_ip}::INSTR', True, False)
                comando = self.comando_entry.get()
                if comando in self.comandos_sem_resposta:
                    instr.write(comando)
                    log_entry = f"Enviado: {comando}\nRecebido: Comando enviado com sucesso (sem resposta esperada).\n"
                elif comando.endswith('?'):
                    resposta = instr.query(comando)
                    log_entry = f"Enviado: {comando}\nRecebido: {resposta}\n"
                else:
                    instr.write(comando)
                    log_entry = f"Enviado: {comando}\nRecebido: Comando enviado com sucesso.\n"
                
                self.log_text.insert(tk.END, log_entry)
                self.comando_entry.delete(0, tk.END)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set.\n{e}")
        else:
            messagebox.showerror("Error", "IP not set. Please connect to an instrument first.")  # Janela de comando para teste           


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
