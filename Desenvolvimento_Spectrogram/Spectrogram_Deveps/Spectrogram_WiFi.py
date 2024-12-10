#Assim que concluido, preciso simplificar esse codigo
#o codigo precisa de mais funcoes que o simplifiquem 

#Alguns commandos: 
# INST:SEL SAN = Seleciona a funcao spectrumm Analizer
from audioop import avgpp
import dbm
from msilib.schema import _Validation_records
import re
import time
import csv
from datetime import datetime
from tkinter import *
import os
import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu, StringVar
from token import COMMA
from RsInstrument.Internal.Instrument import Conv
from RsInstrument.RsInstrument import RsInstrument

TechnologyModulations = [
        "IEEE 802.11a", "IEEE 802.11b", "IEEE 802.11g", 
        "IEEE 802.11n", "IEEE 802.11n (40)", "IEEE 802.11ac",
        "IEEE 802.11ac (40)", "IEEE 802.11ac (80)", 
        "IEEE 802.11ac (160)", "IEEE 802.11ax", 
        "IEEE 802.11ax (40)", "IEEE 802.11ax (80)", 
        "IEEE 802.11ax (160)", "IEEE 802.11be", 
        "IEEE 802.11be (40)", "IEEE 802.11be (80)", 
        "IEEE 802.11be (160)", "IEEE 802.11be (320)"
    ]

REF_LEV = [
    "-10 dBm", "-5 dBm", "0 dBm",
    "5 dBm", "10 dBm", "15 dBm",
    "20 dBm", "25 dBm", "30 dBm",
    "35 dBm", "40 dBm", "45 dBm"
    ]


class MainProgram(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("550x800")
        self.title("Spectrogram Wi-Fi")
        self.create_widgets_TestConnection()
        self.Data_Screen()
        self.Preset_Screen()


    def create_widgets_TestConnection(self):
        self.fonte = ("Verdana", "8")

        self.Container_1 = LabelFrame(text="Instrument Connection", padx=10, pady=10)
        self.Container_1.pack(side=TOP)

        self.FirthPackIP = Frame(self.Container_1)
        self.FirthPackIP.pack(side=TOP)

        self.LABIP = Label(self.FirthPackIP, text="IP", font=("Calibri", "12", "bold"))
        self.LABIP.pack(side=LEFT)

        self.EntradaIP = Entry(self.FirthPackIP, font=("Arial", "10"), width=15)
        self.EntradaIP.pack(side=LEFT)

        self.ConnectingButton = Button(self.FirthPackIP, text="Connect", command=self.authenticate, font=("Calibri", "10"), width=15)
        self.ConnectingButton.pack(side=RIGHT)

        self.Container_2 = LabelFrame(self.Container_1, text="Dados do equipamento", pady=5)
        self.Container_2.pack(side=TOP)

        self.lb = Listbox(self.Container_2, width=45, height=6)
        self.lb.pack(side=TOP, expand=True)

        self.Container_3 = Frame(self.Container_1, padx=10, pady=10)
        self.Container_3.pack()

    def authenticate(self):
        self.ip_val = self.EntradaIP.get()
        try:
            self.resource_string_1 = f'TCPIP::{self.ip_val}::INSTR'
            self.instr = RsInstrument(self.resource_string_1, True, False)
            self.idn = self.instr.query_str('*IDN?')
            self.driver = self.instr.driver_version
            self.visa_manufacturer = self.instr.visa_manufacturer
            self.instrument_full_name = self.instr.full_instrument_model_name

            info = f"Name: {self.idn}\nRsInstrument Driver Version: {self.driver}\nVisa Manufacturer: {self.visa_manufacturer}\nInstrument Full Name: {self.instrument_full_name}"
            messagebox.showinfo("Instrument informations", info)
            self.info_instrument()
        except Exception as e:
            messagebox.showerror("Error", f"Connections Fail!\n{e}")
            self.lb.delete(0, END)

    def info_instrument(self):
        self.lb.insert(END, 'Name: ' + self.idn)
        self.lb.insert(END, 'RsInstrument Driver Version: ' + self.driver)
        self.lb.insert(END, 'Visa Manufacturer: ' + self.visa_manufacturer)
        self.lb.insert(END, 'Instrument full name: ' + self.instrument_full_name)
        self.lb.insert(END, 'Instrument Installed Options: ' + ",".join(self.instr.instrument_options))
        self.lb.insert(END, "Connection Success")
        self.lb.itemconfig(END, {'fg': 'green'})

    def Data_Screen(self):        
        self.Frameinformation = LabelFrame(text="Dados da amostra", padx=10, pady=10)
        self.Frameinformation.pack(side=TOP)        

        self.ProtocoloLabel = Label(self.Frameinformation, text="Protocolo: ", font=("Calibri","12"))
        self.ProtocoloLabel.grid(row=0, column=0, sticky="w", padx=(0,10))
        
        self.ProtocolEntry = Entry(self.Frameinformation, font=("Arial", "10"), width= 16)
        self.ProtocolEntry.grid(row=0, column=1,sticky="w", padx=(0,10))
        
        self.FileDestineLabel = Label(self.Frameinformation, text="Selecione a pasta de destino", font=("Calibri","12"))
        self.FileDestineLabel.grid(row = 1, column=0, sticky="w",padx=(0,10))
        
        self.Button_Fille = Button(self.Frameinformation,text="Select file", command=self.Print_screen_File, font=("Calibri", "10"), width=15)
        self.Button_Fille.grid(row=1,column=1, sticky="w",padx=(0,10))

        self.FilePath = Entry(self.Frameinformation, font=("Arial", "10"), width= 35)
        self.FilePath.grid(row=2, column=0,columnspan=2, sticky="we", padx=(0,10))

    def Preset_Screen(self):
        self.CheckPot5G_bool = tk.BooleanVar()
        self.CheckDen5G_bool = tk.BooleanVar()
        self.Check_Largura6dB = tk.BooleanVar()
        self.Check_Largura26dB = tk.BooleanVar()
        self.Check_PotPicMax = tk.BooleanVar()
        self.Check_Densidade_Spec = tk.BooleanVar()
        self.Check_Esp = tk.BooleanVar()
        self.Check_Prints = tk.BooleanVar()

        self.CheckFreqInic = tk.BooleanVar()
        self.CheckFreqCent = tk.BooleanVar()
        self.CheckFreqFina = tk.BooleanVar()
        
        self.Check5G = tk.BooleanVar()
        
        
        self.CheckPrint_Init = tk.BooleanVar()
        self.CheckPrint_Cent = tk.BooleanVar()
        self.CheckPrint_Fina = tk.BooleanVar()

        self.TIMERSET = tk.BooleanVar()

        self.RefLevel = StringVar(self)

        self.CheckRefLevel = tk.BooleanVar()

        self.TechnologyChose = StringVar(self)
        self.TechnologyChose.set("IEEE 802.11b")

        
        self.FramePreset = LabelFrame(text="Preset do ensaio", padx=10, pady=10)
        self.FramePreset.pack(side=TOP)    
        
        self.TechnologySelectLabel = Label(self.FramePreset, text="Selecione a tecnologia: ", font=("Calibri","12"))
        self.TechnologySelectLabel.grid(row=0, column=0, sticky="w", padx=(0,10))  
        
        self.TechnologySelect = OptionMenu(self.FramePreset, self.TechnologyChose, *TechnologyModulations)
        self.TechnologySelect.grid(row=0, column=1, sticky="e", padx=(0, 10))

        self.FrameTest_Select = LabelFrame(self.FramePreset, text="Selecao dos testes", padx=10, pady=10)
        self.FrameTest_Select.grid(row=1, column=0, sticky="w",columnspan=2, padx=(0,10)) 

        # Potencia na saida do transmissor 5G
        self.Pot_5G_Label = Label(self.FrameTest_Select, text="Potencia na saida do transmissor", font=("Calibri","12"),state="disabled")
        self.Pot_5G_Label.grid(row=0, column=0, sticky="w", padx=(0,10))
        
        self.CheckPot_5G = tk.Checkbutton(self.FrameTest_Select,variable=self.CheckPot5G_bool,state="disabled")
        self.CheckPot_5G.grid(row=0, column=5, sticky="w")  

        # Densisdade media de potencia 5G
        self.Den_5G_Label = Label(self.FrameTest_Select, text="Densidade media de potencia ", font=("Calibri","12"),state="disabled")
        self.Den_5G_Label.grid(row=1, column=0, sticky="w", padx=(0,10))
        
        self.CheckDen_5G = tk.Checkbutton(self.FrameTest_Select,variable=self.CheckDen5G_bool,state="disabled")
        self.CheckDen_5G.grid(row=1, column=5, sticky="w")  

        # Largura de faixa a 6dBm  
        self.Larg6dB_Label = Label(self.FrameTest_Select, text="Largura de faixa a 6dB", font=("Calibri","12"))
        self.Larg6dB_Label.grid(row=2, column=0, sticky="w", padx=(0,10))
        
        self.CheckLarg6dB = tk.Checkbutton(self.FrameTest_Select,variable=self.Check_Largura6dB)
        self.CheckLarg6dB.grid(row=2, column=5, sticky="w")  

        # Largura de faixa a 26dBm  
        self.Larg26dB_Label = Label(self.FrameTest_Select, text="Largura de faixa a 26dB", font=("Calibri","12"))
        self.Larg26dB_Label.grid(row=3, column=0, sticky="w", padx=(0,10))
        
        self.CheckLarg26dB = tk.Checkbutton(self.FrameTest_Select,variable=self.Check_Largura26dB)
        self.CheckLarg26dB.grid(row=3, column=5, sticky="w")  
        # Potencia de pico maximo
        self.PotPic_Label = Label(self.FrameTest_Select, text="Potencia de pico maximo", font=("Calibri","12"))
        self.PotPic_Label.grid(row=4, column=0, sticky="w", padx=(0,10))
        
        self.CheckPotPic = tk.Checkbutton(self.FrameTest_Select,variable=self.Check_PotPicMax)
        self.CheckPotPic.grid(row=4, column=5, sticky="w")  
        # Densidade
        self.Densidade_Label = Label(self.FrameTest_Select, text="Densidade Espectral", font=("Calibri","12"))
        self.Densidade_Label.grid(row=5, column=0, sticky="w", padx=(0,10))
        
        self.CheckDensid_Esp = tk.Checkbutton(self.FrameTest_Select,variable=self.Check_Densidade_Spec)
        self.CheckDensid_Esp.grid(row=5, column=5, sticky="w")  
        # Espurios
        self.Espurios_Label = Label(self.FrameTest_Select, text="Espurios", font=("Calibri","12"))
        self.Espurios_Label.grid(row=6, column=0, sticky="w", padx=(0,10))
        
        self.CheckEspurios = tk.Checkbutton(self.FrameTest_Select,variable=self.Check_Esp)
        self.CheckEspurios.grid(row=6, column=5, sticky="w")  
        

        #Label Frequencia
        self.FrameFrequencia = LabelFrame(self.FramePreset, text="Frequencia", padx=10, pady=10)
        self.FrameFrequencia.grid(row=2, column=0, sticky="w",columnspan=3, padx=(0,10)) 

        self.CheckFrequenciaInicial = tk.Checkbutton(self.FrameFrequencia,variable=self.CheckFreqInic, command=self.toggle_checkbox_Start)
        self.CheckFrequenciaInicial.grid(row=0, column=0, sticky="w")  
        
        self.FrequenciaInicial_Label = Label(self.FrameFrequencia, text="Frequencia Inicial", font=("Calibri","12"))
        self.FrequenciaInicial_Label.grid(row=0, column=1, sticky="w", padx=(0,10))
     
        self.Frequencia_Inicial_Entry = Entry(self.FrameFrequencia, font=("Arial", "10"), width= 7)
        self.Frequencia_Inicial_Entry.grid(row=0, column=2, sticky="w", padx=(0,10))  
         
        self.UnitFreq_Label = Label(self.FrameFrequencia, text="MHz", font=("Calibri","12"))
        self.UnitFreq_Label.grid(row=0, column=3, sticky="w", padx=(0,10))
        
        self.CheckFrequenciaInicialPrint = tk.Checkbutton(self.FrameFrequencia,variable=self.CheckPrint_Init)
        self.CheckFrequenciaInicialPrint.grid(row=0, column=4, sticky="w")  

        self.PrintLabel = Label(self.FrameFrequencia, text="Prints", font=("Calibri","12"))
        self.PrintLabel.grid(row=0, column=5, sticky="w", padx=(0,10))





        self.CheckFrequenciaCentral = tk.Checkbutton(self.FrameFrequencia,variable=self.CheckFreqCent,command=self.toggle_checkbox_Center)
        self.CheckFrequenciaCentral.grid(row=1, column=0, sticky="w")  
        
        self.FrequenciaCentral_Label = Label(self.FrameFrequencia, text="Frequencia Central", font=("Calibri","12"))
        self.FrequenciaCentral_Label.grid(row=1, column=1, sticky="w", padx=(0,10))
       
        self.Frequencia_Central_Entry = Entry(self.FrameFrequencia, font=("Arial", "10"), width= 7)
        self.Frequencia_Central_Entry.grid(row=1, column=2, sticky="w", padx=(0,10))         

        self.UnitFreq_Label = Label(self.FrameFrequencia, text="MHz", font=("Calibri","12"))
        self.UnitFreq_Label.grid(row=1, column=3, sticky="w", padx=(0,10))

        self.CheckFrequenciaCentralPrint = tk.Checkbutton(self.FrameFrequencia,variable=self.CheckPrint_Cent)
        self.CheckFrequenciaCentralPrint.grid(row=1, column=4, sticky="w")  

        self.PrintLabel = Label(self.FrameFrequencia, text="Prints", font=("Calibri","12"))
        self.PrintLabel.grid(row=1, column=5, sticky="w", padx=(0,10))





        self.CheckFrequenciaFinal = tk.Checkbutton(self.FrameFrequencia,variable=self.CheckFreqFina,command=self.toggle_checkbox_Finale)
        self.CheckFrequenciaFinal.grid(row=2, column=0, sticky="w")  

        self.FrequenciaFinal_Label = Label(self.FrameFrequencia, text="Frequencia Final", font=("Calibri","12"))
        self.FrequenciaFinal_Label.grid(row=2, column=1, sticky="w", padx=(0,10))

        self.Frequencia_Final_Entry = Entry(self.FrameFrequencia, font=("Arial", "10"), width= 7)
        self.Frequencia_Final_Entry.grid(row=2, column=2, sticky="w", padx=(0,10))    
        
        self.UnitFreq_Label = Label(self.FrameFrequencia, text="MHz", font=("Calibri","12"))
        self.UnitFreq_Label.grid(row=2, column=3, sticky="w", padx=(0,10))

        self.CheckFrequenciaFinalPrint = tk.Checkbutton(self.FrameFrequencia,variable=self.CheckPrint_Fina)
        self.CheckFrequenciaFinalPrint.grid(row=2, column=4, sticky="w")      

        self.PrintLabel = Label(self.FrameFrequencia, text="Prints", font=("Calibri","12"))
        self.PrintLabel.grid(row=2, column=5, sticky="w", padx=(0,10))
        
        #Frame Start
        self.FrameCommand = LabelFrame(self.FramePreset, text="Inicializacao do ensaio", padx=10, pady=10)
        self.FrameCommand.grid(row=3, column=0, sticky="w",columnspan=3, padx=(0,10)) 

        self.Button_Start = Button(self.FrameCommand,text="START", command=self.Start, font=("Calibri", "10"), width=15)
        self.Button_Start.grid(row=1,column=0, sticky="w",columnspan=4,padx=(0,10))
        
        self.Timer_Label = Label(self.FrameCommand, text="Timer", font=("Calibri","12"))
        self.Timer_Label.grid(row=2, column=0, sticky="w", padx=(0,5))

        self.Timer_Entry = Entry(self.FrameCommand, font=("Arial", "10"), width= 3)
        self.Timer_Entry.grid(row=2, column=1, sticky="w", padx=(0,5))  
        
        self.Timer_Label = Label(self.FrameCommand, text="Seg", font=("Calibri","10"))
        self.Timer_Label.grid(row=2, column=2, sticky="e", padx=(0,5))

        self.ActiveTIMER = tk.Checkbutton(self.FrameCommand,variable=self.TIMERSET)
        self.ActiveTIMER.grid(row=2, column=3, sticky="e")  


        #Frame Configs medidas
        self.FrameConfig = LabelFrame(self.FramePreset, text="Configs", padx=10, pady=10)
        self.FrameConfig.grid(row=3, column=1, sticky="w",columnspan=3, padx=(0,10)) 

        self.Ensaios5G_Label = Label(self.FrameConfig, text="5.2/5.4 GHz", font=("Calibri","12"))
        self.Ensaios5G_Label.grid(row=0, column=0, sticky="w", padx=(0,10))

        self.Check5GHz = tk.Checkbutton(self.FrameConfig,variable=self.Check5G, command=self.toggle_checkbox_5G)
        self.Check5GHz.grid(row=0, column=1, sticky="w")  

        self.REFLEVEL_Label = Label(self.FrameConfig, text="Ref Lev manual", font=("Calibri","12"))
        self.REFLEVEL_Label.grid(row=1, column=0, sticky="w", padx=(0,10))

        self.Amp_Select = OptionMenu(self.FrameConfig, self.RefLevel, *REF_LEV)
        self.Amp_Select.grid(row=1, column=1, sticky="e", padx=(0, 10))

        self.CheckRefLev = tk.Checkbutton(self.FrameConfig,variable=self.CheckRefLevel)
        self.CheckRefLev.grid(row=1, column=2, sticky="w")  



    def PresetsforTest(self, Reset, RBW, UnitRBW, VBW, UnitVBW, SPAN, DISPLAY, ATT, SWEEP_COUNT,SWEEP_MODE, FREQ, TRACE,AVGMOD,DETECTOR, functions):
        TEMPO = int(self.TIMERSET.get())
        SelectDetector = ["DET APE","DET POS","DET NEG","DET SAMP","DET RMS","DET AVER","DET QPE"]
        AVG_MODS = ["","SENS:AVER1:TYPE LIN"]
        ListRBW = ["Hz", "kHz", "MHz", "GHz"]
        ListVBW = ["Hz", "kHz", "MHz", "GHz"]
        StatusRESET = ["*RST", ""]
        StatusDisplay = ["SYST:DISP:UPD OFF", "SYST:DISP:UPD ON"]
        ListTRACE = [
            "DISP:WIND:TRAC:MODE WRIT", "DISP:WIND:TRAC:MODE MAXH",
            "DISP:WIND:TRAC:MODE AVER", "DISP:WIND:TRAC:MODE VIEW"
        ]
        ListSWEEP_MODE = ["INIT:CONT OFF; :INIT","INIT:CONT ON"]
        ListSWEEP = f"SENS:SWE:COUN {SWEEP_COUNT}"
        self.instr.visa_timeout = 30000  # Timeout de 60 segundos
        self.command_template([
            StatusDisplay[DISPLAY],
            StatusRESET[Reset],
            ListSWEEP_MODE[SWEEP_MODE],            
            ListSWEEP,
            SelectDetector[DETECTOR],     
            f"BAND:VID {VBW} {ListVBW[UnitVBW]}",
            f"BAND {RBW} {ListRBW[UnitRBW]}",
            f"FREQ:CENT {FREQ} MHz",
            ListTRACE[TRACE],
            AVG_MODS[AVGMOD], 
            f"INP:ATT {ATT} DB",
            f"DISP:WIND:TRAC:Y:RLEV {self.RefLevel_Preset}",
            f"FREQ:SPAN {SPAN} MHz",
            "INIT:IMM"
        ])
        if functions == 0:# Largura de faixa a 6dBm
            self.command_template(["CALC:MARK:FUNC:POW:SEL OBW","SENS:POW:BWID 99 PCT",])
            time.sleep(self.TimerCount_Void(TEMPO))
            self.instr.write_str("CALC:MARK1:MAX")
            self.Results = self.convert_hz_to_mhz(self.instr.query_str("CALC:MARK:FUNC:POW:RES? OBW"))
            print(self.instr.query_str("CALC:MARK:FUNC:POW:RES? OBW"))
            print(self.Results)
        if functions == 1:# Largura de faixa a 26dBm
            self.command_template(["CALC:MARK:FUNC:POW:SEL OBW","SENS:POW:BWID 99.9 PCT"])
            time.sleep(self.TimerCount_Void(self.TIMERSET.get()))
            self.instr.write_str("CALC:MARK1:MAX")
            self.Results = self.convert_hz_to_mhz(self.instr.query_str("CALC:MARK:FUNC:POW:RES? OBW"))
        if functions == 2:# Potencia de pico maximo
            self.command_template(["CALC:MARK:FUNC:POW:SEL CPOW",f"SENS:POW:ACH:BWID:CHAN {self.Bandwidth} MHz",f"FREQ:SPAN {SPAN} MHz"])
            time.sleep(self.TimerCount_Void(self.TIMERSET.get()))
            self.Results = self.convert_hz_to_mhz(self.instr.query_str("CALC:MARK:FUNC:POW:RES? CPOW"))
        if functions == 3:# Pico da densidade de potencia / Densidade em 5G (Uso da mesma funcao)
            self.instr.write_str("INIT;*WAI")
            self.command_template(["CALC:MARK:MAX"])
            self.Results = self.instr.query("CALC:MARK:Y?")
        if functions == 4:# Potencia 5G
            self.command_template(["CALC:MARK:FUNC:POW:SEL CPOW",f"SENS:POW:ACH:BWID:CHAN {self.Bandwidth} MHz",f"FREQ:SPAN {SPAN} MHz",f"BAND {RBW} {ListRBW[UnitRBW]}",f"BAND:VID {VBW} {ListVBW[UnitVBW]}",AVG_MODS[AVGMOD],SelectDetector[DETECTOR], ])
            self.command_template(["INIT:CONT OFF"])
            time.sleep(self.TimerCount_Void(self.TIMERSET.get()))
            self.Results = self.converter_valor(self.instr.query_str("CALC:MARK:FUNC:POW:RES? CPOW"))
        self.instr.visa_timeout = 1000
        
    def Start(self):
        FreqStart = self.Frequencia_Inicial_Entry.get()         #
        FreqCenter = self.Frequencia_Central_Entry.get()        #
        FreqFinale = self.Frequencia_Final_Entry.get()          # Sim! Uma tristeza declarar TANTA Variavel numa funcao
        Print_Start = self.CheckPrint_Init.get()                # Vou ver uma forma de resuzir isso aqui
        Print_Center = self.CheckPrint_Cent.get()               #
        Print_Finale = self.CheckPrint_Fina.get()               #
        Start = self.CheckFreqInic.get()                        #
        Center = self.CheckFreqCent.get()                       #
        Finale = self.CheckFreqFina.get()                       #
        try:
            if self.ip_val:
                timetest = self.measure_execution_time(self.GeralTest,FreqStart,FreqCenter,FreqFinale,Print_Start,Print_Center,Print_Finale,Start,Center,Finale)
                messagebox.showinfo("FIM",f"Concluido \n Tempo de teste: {timetest:.3f} Seg")
                self.log_execution_time(self.ProtocolEntry.get(),timetest,self.save_dir)
            else:
                messagebox.showwarning("Erro ao conectar no analisador","Insira o IP do analisador a ser conectado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao na execucao do programa.\n{e}")
        

    def ConversorRapdio(self,Val):
        print(Val)
        Tofloat = {Val:.3}
        print(Tofloat)
        Converter = Tofloat.replace(".",",")
        print(Converter)
        return Converter

    def converter_valor(self,valor):
        # Trunca o valor para 3 casas decimais e substitui o ponto por virgula
        valor_convertido = "{:.3f}".format(float(valor)).replace('.', ',')
        return valor_convertido



    def Start_Sequency(self,Freq,PrinScreen):
        self.Print_Screen_Func(0,False) #Ativa a pasta onde sera salvo os valores
        self.ReferenceSelector(self.CheckRefLevel.get())
        modulation = self.TechnologyChose.get()
        if "(40)" in modulation:
            self.Bandwidth = 40.0
        elif "(80)" in modulation:
            self.Bandwidth = 80.0
        elif "(160)" in modulation:
            self.Bandwidth = 160.0
        elif "(320)" in modulation:
            self.Bandwidth = 320.0
        else:
            self.Bandwidth = 20.0
            
        #funcao das opcoes marcadas: 
        if self.Check_Largura6dB.get():
            self.PresetsforTest(0,"100",1,"300",1,str(float(self.Bandwidth) * 1.5),0,"40",0,1,Freq,1,0,1,0)
            self.Print_Screen_Func("Largura de faixa a 6dB",PrinScreen)
            self.save_test_results(f"{self.tech_path}\Largura_6dB.csv",Freq,self.Results,0)      
            self.Results = None
        if self.Check_Largura26dB.get():
            self.PresetsforTest(0,"100",1,"300",1,str(float(self.Bandwidth) * 1.5),0,"40",0,1,Freq,1,0,1,1)  
            self.Print_Screen_Func("Largura de faixa a 26dB",PrinScreen)   
            self.save_test_results(f"{self.tech_path}\Largura_26dB.csv",Freq,self.Results,0)
            self.Results = None
        if self.Check_PotPicMax.get():
            self.PresetsforTest(0,"1",2,"3",2,str(float(self.Bandwidth) * 1.5),0,"40",0,1,Freq,1,0,1,2)             
            self.Print_Screen_Func("Potencia de pico",PrinScreen)
            self.save_test_results(f"{self.tech_path}\Potencia de pico maximo.csv",Freq,self.Results,1)
            self.Results = None
        if self.Check_Densidade_Spec.get():
            self.PresetsforTest(0,"3",1,"10",1,str(float(self.Bandwidth) * 1.5),0,"40",3,0,Freq,1,0,1,3)  
            self.Print_Screen_Func("Densidade espectral",PrinScreen)                    
            self.save_test_results(f"{self.tech_path}\Densidade espectral de potencia.csv",Freq,f"{float(self.Results):.5}",1)
            self.Results = None
        if self.Check_Esp.get():
            messagebox.showinfo ("Desponivel em breve","Use a automacao Spectrogram_ESP!")
        if self.CheckPot5G_bool.get():
            self.PresetsforTest(0,"1",2,"3",2,str(float(self.Bandwidth) * 1.5),0,"40",100,0,Freq,2,1,4,4)
            self.Print_Screen_Func("Potencia na saida do transmissor",PrinScreen)
            self.save_test_results(f"{self.tech_path}\Potencia na saida do transmissor.csv",Freq,self.Results,1)
            self.Results = None                   
        if self.CheckDen5G_bool.get():
            self.PresetsforTest(0,"1",2,"3",2,str(float(self.Bandwidth) * 1.5),0,"40",100,0,Freq,2,1,4,4)
            self.instr.write_str("INIT;*WAI")
            self.command_template(["CALC:MARK:MAX"])
            self.Results = self.instr.query("CALC:MARK:Y?")
            Dot_to_virgula = self.Results.replace(".",",")
            self.save_test_results(f"{self.tech_path}\Densidade media de potencia.csv",Freq,f"{Dot_to_virgula:.5}",1)
            self.Results = None    
            
    def measure_execution_time(self, func, *args, **kwargs): #Retorna o tempo de execucao da operacao total
        if not callable(func):
            raise ValueError("O parametro 'func' deve ser uma funcao ou metodo chamavel.")
        # Captura o tempo de inicio
        start_time = time.time()
        # Executa a funcao com os argumentos fornecidos
        func(*args, **kwargs)
        # Captura o tempo de termino
        end_time = time.time()
        # Calcula o tempo total de execucao
        execution_time = end_time - start_time
        # Retorna o tempo de execucao formatado
        print(f"Tempo de execucao: {execution_time:.3f} segundos")
        return execution_time
    
    def ReferenceSelector(self,State):
        if State:
            self.RefLevel_Preset = self.RefLevel.get()
        elif not State:
            self.RefLevel_Preset = "30 dbm"

    def GeralTest(self,StartFreq,CenterFreq,FinaleFreq,PrintStart,PrintCenter,PrintFinale,ValueStart,ValueCenter,ValueFinale):
        if not ValueStart:
            messagebox.showinfo ("Frequencia inicial da amostra","Frequencia inicial da amostra Selecionada. Ajuste o ESE!")
            self.Start_Sequency(StartFreq,PrintStart)
        if not ValueCenter:
            messagebox.showinfo ("Frequencia Central da amostra","Frequencia Central da amostra Selecionada. Ajuste o ESE!")
            self.Start_Sequency(CenterFreq,PrintCenter)
        if not ValueFinale:  
            messagebox.showinfo ("Frequencia Final da amostra","Frequencia Final da amostra Selecionada. Ajuste o ESE!")
            self.Start_Sequency(FinaleFreq,PrintFinale)
        if ValueStart & ValueCenter & ValueFinale:
            messagebox.showwarning ("Nenhuma frequencia selecionada","Selecione agluma frequencia para executar o programa!")
            
    def toggle_checkbox_Start(self):
        # Verifica o estado do primeiro checkbox
        if self.CheckFreqInic.get():
            self.CheckFrequenciaInicialPrint.config(state="disabled")  # Desabilita o segundo checkbox
            self.Frequencia_Inicial_Entry.delete(0, END)
            self.Frequencia_Inicial_Entry.config(state="disabled")
            self.CheckPrint_Init.set(False)
        else:
            self.CheckFrequenciaInicialPrint.config(state="normal")  # Habilita o segundo checkbox
            self.Frequencia_Inicial_Entry.config(state="normal")
            
    def toggle_checkbox_Center(self):
        # Verifica o estado do primeiro checkbox
        if self.CheckFreqCent.get():
            self.CheckFrequenciaCentralPrint.config(state="disabled")  # Desabilita o segundo checkbox
            self.Frequencia_Central_Entry.delete(0, END)
            self.Frequencia_Central_Entry.config(state="disabled")
            self.CheckPrint_Cent.set(False)
        else:
            self.CheckFrequenciaCentralPrint.config(state="normal")  # Habilita o segundo checkbox
            self.Frequencia_Central_Entry.config(state="normal")
            
    def toggle_checkbox_Finale(self):
        # Verifica o estado do primeiro checkbox
        if self.CheckFreqFina.get():
            self.CheckFrequenciaFinalPrint.config(state="disabled")  # Desabilita o segundo checkbox
            self.Frequencia_Final_Entry.delete(0, END)
            self.Frequencia_Final_Entry.config(state="disabled")
            self.CheckPrint_Fina.set(False)
        else:
            self.CheckFrequenciaFinalPrint.config(state="normal")  # Habilita o segundo checkbox
            self.Frequencia_Final_Entry.config(state="normal")
    
    def toggle_checkbox_5G(self):
        if self.Check5G.get():
            self.CheckPot_5G.config(state="normal")
            self.Pot_5G_Label.config(state="normal")
            self.CheckDen_5G.config(state="normal")            
            self.Den_5G_Label.config(state="normal")
            self.CheckLarg6dB.config(state="disabled")
            self.CheckLarg26dB.config(state="disabled")
            self.CheckPotPic.config(state="disabled")
            self.CheckDensid_Esp.config(state="disabled")
            self.CheckEspurios.config(state="disabled")
            self.Check_Largura6dB.set(False)
            self.Check_Largura26dB .set(False)
            self.Check_PotPicMax.set(False)
            self.Check_Densidade_Spec.set(False)
            self.Check_Esp.set(False)
            
        else:   
            self.CheckLarg6dB.config(state="normal")
            self.CheckLarg26dB.config(state="normal")
            self.CheckPotPic.config(state="normal")
            self.CheckDensid_Esp.config(state="normal")
            self.CheckEspurios.config(state="normal")
            self.CheckPot_5G.config(state="disabled")
            self.Pot_5G_Label.config(state="disabled")
            self.CheckDen_5G.config(state="disabled")
            self.Den_5G_Label.config(state="disabled")            
            self.CheckPot5G_bool.set(False)
            self.CheckDen5G_bool.set(False)
            
    def TimerCount_Void(self,Switch):
        TIMERSET = self.Timer_Entry.get()
        if Switch:
            return int(TIMERSET)
        else:
            return 1.5

    def log_execution_time(self,protocolo, tempo_execucao, diretorio):
        """
        Grava tempos de execucao em um arquivo CSV com o nome [protocolo]_Tempos_de_Teste.csv.

        :param protocolo: Nome do protocolo utilizado.
        :param tempo_execucao: Tempo de execucao em segundos.
        :param diretorio: Caminho do diretorio onde o arquivo sera salvo.
        """
        # Nome do arquivo
        nome_arquivo = os.path.join(diretorio, f"{protocolo}_Tempos_de_Teste.csv")

        # Obter data e hora atuais
        agora = datetime.now()
        data_atual = agora.strftime("%d/%m/%Y")
        hora_atual = agora.strftime("%H:%M")

        # Verificar se o arquivo ja existe
        arquivo_existe = os.path.isfile(nome_arquivo)

        # Abrir o arquivo para escrita (adiciona dados caso o arquivo ja exista)
        with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # Escrever cabecalho se o arquivo for novo
            if not arquivo_existe:
                writer.writerow(["Index", "Tempo [Seg]", "Data", "Hora"])

            # Obter o proximo indice
            if arquivo_existe:
                with open(nome_arquivo, mode='r', encoding='utf-8') as readfile:
                    index = sum(1 for _ in readfile) - 1  # Conta linhas e subtrai o cabecalho
            else:
                index = 0

            # Escrever a nova linha com dados
            index += 1
            writer.writerow([index, f"{tempo_execucao:.3f}".replace('.', ','), data_atual, hora_atual])

        print(f"Dados salvos no arquivo: {nome_arquivo}")

    def convert_hz_to_mhz(self,hz_value_str):
        # Remove separadores de milhar (por exemplo, virgulas ou pontos)
        apenas_numeros = re.findall(r'\d', hz_value_str)
        oito_digitos = ''.join(apenas_numeros[:8])
        # Converte a string para float
        try:
            hz_value = float(oito_digitos)
        except ValueError:
            raise ValueError("O valor fornecido nao e um numero valido.")
        
        # Primeiro, converte de Hz para MHz
        value_in_mhz = hz_value / 1_000_000
        # Corrige o deslocamento da virgula dividindo por 1000
        corrected_value_in_mhz = value_in_mhz / 1
    
    # Formata o valor com a virgula como separador de milhar e ponto como separador decimal
        formatted_value = f"{corrected_value_in_mhz:,.4f}".replace('.', ',')
        return formatted_value

    def command_template(self, commands):
        for command in commands:
            self.instr.write_str(command)

    def Print_screen_File(self):
        default_dir = r"C:\\"
        if messagebox.askyesno("Escolha do Diretorio", "Deseja escolher o local para salvar o print?"):
          self.save_dir = filedialog.askdirectory(title="Selecione o diretorio para salvar o print")
          if self.save_dir:
            self.FilePath.delete(0, END)
            self.FilePath.insert(0, self.save_dir)
          if not self.save_dir:
              messagebox.showerror("Erro", "Nenhum diretorio selecionado. Cancelando operacao.")
              return
        else:
          self.save_dir = default_dir
       
    def Print_Screen_Func(self, IndexPrint,state):
        try:
            if self.ip_val:
                try:
                    # Captura o timestamp para o nome do arquivo
                    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
                    Protocolo = self.ProtocolEntry.get()
                    TechnologyGet = self.TechnologyChose.get()
                    
                    # Verifica se a pasta da tecnologia ja existe; se nao, cria
                    self.tech_path = os.path.join(self.save_dir, TechnologyGet)
                    if not os.path.exists(self.tech_path):
                        os.makedirs(self.tech_path)
                    if state:
                        # Cria o caminho completo para salvar o print
                        self.save_path = os.path.join(self.tech_path, f"{IndexPrint}_{TechnologyGet}_{Protocolo}_{timestamp}.png")
                        
                        # Envia comandos para capturar e salvar o print
                        instr = RsInstrument(f'TCPIP::{self.ip_val}::INSTR', True, False)
                        instr.write_str('HCOP:DEST "MMEM"')  # Enviar print para a memoria interna
                        instr.write_str(f'MMEM:NAME "C:\\Temp\\screen.bmp"')  # Nome temporario no FSMR
                        instr.write_str('HCOP:IMM')  # Capturar a tela imediatamente
                        instr.query_bin_block_to_file('MMEM:DATA? "C:\\Temp\\screen.bmp"', self.save_path)  # Baixar o arquivo do FSMR
                    else:
                        return
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao salvar o print.\n{e}")
                finally:
                    if state:
                        instr.close()
            else:
                messagebox.showerror("Erro", "IP nao configurado. Conecte-se a um instrumento primeiro.")
        except:
            messagebox.showerror("Erro", "IP nao configurado. Conecte-se a um instrumento primeiro.")

    def save_test_results(self,file_name, frequency, test_value, TestType):
        #
        #Salva os resultados dos testes em um arquivo CSV, substituindo valores
        #repetidos de frequencia com os novos.
        #
        #:param file_name: Nome do arquivo CSV (incluindo a extensao .csv).
        #:param frequency: Frequencia em MHz.
        #:param test_value: Valor do teste em MHz ou dBm.
        #:param TestType: Tipo do teste (0 para MHz, 1 para dBm).
        #
        current_datetime = datetime.now().strftime("%d-%m-%Y")
        new_data = [str(frequency), str(test_value), current_datetime]
    
        # Verifica se o arquivo ja existe
        if os.path.isfile(file_name):
            # Le os dados existentes
            with open(file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                rows = list(reader)
    
            # Atualiza os dados existentes ou adiciona novos
            header = rows[0]  # Mantem o cabecalho
            updated = False
    
            for i in range(1, len(rows)):
                if rows[i][0] == str(frequency):  # Frequencia igual
                    rows[i] = new_data  # Substitui a linha
                    updated = True
                    break
            
            if not updated:
                rows.append(new_data)  # Adiciona se nao encontrar a frequencia
            
            # Reescreve o arquivo CSV com os dados atualizados
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(rows)
        else:
            # Cria um novo arquivo e adiciona o cabecalho
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                if TestType == 0:
                    writer.writerow(["frequencia [MHz]", "Valor do teste [MHz]", "Data"])
                elif TestType == 1:
                    writer.writerow(["frequencia [MHz]", "Valor do teste [dBm]", "Data"])
                writer.writerow(new_data)


def main():
    app = MainProgram() 
    app.mainloop()

if __name__ == "__main__":
    main()
