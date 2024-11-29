from ast import Return
from cProfile import label
import time
from pickle import PROTO
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import os
from tkinter import filedialog
from logging import root
from tkinter import font
from token import NAME
from turtle import st
from RsInstrument.RsInstrument import RsInstrument
import tkinter as tk
from tkinter import LabelFrame, Label, Entry, OptionMenu, StringVar, TOP


# Dicionario que mapeia tecnologias para seus arrays de modulacoes
TechnologyModulations = {
    "Bluetooth BR-EDR": ["GFSK", "8DQPSK", "PI-4DQPSK"],
    "Bluetooth Low Energy": ["BLE 1M", "BLE 2M"],
    "Wi-Fi": [
        "IEEE 802.11a", "IEEE 802.11b", "IEEE 802.11g", 
        "IEEE 802.11n", "IEEE 802.11n (40)", "IEEE 802.11ac",
        "IEEE 802.11ac (40)", "IEEE 802.11ac (80)", 
        "IEEE 802.11ac (160)", "IEEE 802.11ax", 
        "IEEE 802.11ax (40)", "IEEE 802.11ax (80)", 
        "IEEE 802.11ax (160)", "IEEE 802.11be", 
        "IEEE 802.11be (40)", "IEEE 802.11be (80)", 
        "IEEE 802.11be (160)", "IEEE 802.11be (320)"
    ],
    "LoRa": ["LoRa WAN", "LoRa PHY"],
    "Proprietaria": ["GFSK-Prop"],
    "ZigBee": ["O-QPSK"],  
    "ZigFox": ["DBPSK","GFSK"]
}

State_Print = []

class MainProgram(tk.Tk):  # Herdando de Tk em vez de Toplevel
    def __init__(self):
        super().__init__()  # Inicializa o Tk
        self.geometry("450x550")
        self.title("Spectrogram ESP")
        
        self.create_widgets_TestConnection()
        self.ConfiguacoesEspurios()
        self.LabelStartSequence()

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
            idn = self.instr.query_str('*IDN?')
            driver = self.instr.driver_version
            visa_manufacturer = self.instr.visa_manufacturer
            instrument_full_name = self.instr.full_instrument_model_name

            info = f"Name: {idn}\nRsInstrument Driver Version: {driver}\nVisa Manufacturer: {visa_manufacturer}\nInstrument Full Name: {instrument_full_name}"
            messagebox.showinfo("Instrument informations", info)
        except Exception as e:
            messagebox.showerror("Error", f"Connections Fail!\n{e}")
            self.lb.delete(0, END)
            return
        else:
            self.lb.delete(0, END)
            self.info_instrument()

    def info_instrument(self):
        self.ip_val = self.EntradaIP.get()
        resource_string_1 = f'TCPIP::{self.ip_val}::INSTR'
        instr = RsInstrument(resource_string_1, True, False)
        idn = instr.query_str('*IDN?')
        driver = instr.driver_version
        visa_manufacturer = instr.visa_manufacturer
        instrument_full_name = instr.full_instrument_model_name

        self.lb.insert(END, 'Name: ' + idn)
        self.lb.insert(END, 'RsInstrument Driver Version: ' + driver)
        self.lb.insert(END, 'Visa Manufacturer: ' + visa_manufacturer)
        self.lb.insert(END, 'Instrument full name: ' + instrument_full_name)
        self.lb.insert(END, 'Instrument Installed Options: ' + ",".join(instr.instrument_options))
        self.lb.insert(END, "Connection Success")
        self.lb.itemconfig(END, {'fg': 'green'})

    def ConfiguacoesEspurios(self):
        self.CheckState_5G = tk.BooleanVar()

        self.TechnologyChose = StringVar(self)
        self.TechnologyChose.set("Wi-Fi")  # Valor inicial

        self.ModulationChose = StringVar(self)
        self.ModulationChose.set("")  # Inicialmente vazio
        
        self.FrameConfig = LabelFrame(text="Configuracao para espurios", padx=10, pady=10)
        self.FrameConfig.pack(side=TOP)        

        self.ProtocoloLabel = Label(self.FrameConfig, text="Protocolo: ", font=("Calibri","12"))
        self.ProtocoloLabel.grid(row=0, column=0, sticky="w", padx=(0,10))
        
        self.ProtocolEntry = Entry(self.FrameConfig, font=("Arial", "10"), width= 20)
        self.ProtocolEntry.grid(row=0, column=1,sticky="w", padx=(0,10))
        
        # Menu para selecao de tecnologia
        self.TechnologyLabel = Label(self.FrameConfig, text="Selecione a tecnologia: ", font=("Calibri", "12"))
        self.TechnologyLabel.grid(row=1, column=0, sticky="w", padx=(0, 10))

        self.TechnologySelect = OptionMenu(self.FrameConfig, self.TechnologyChose, *TechnologyModulations.keys(), command=self.update_modulations)
        self.TechnologySelect.grid(row=1, column=1, sticky="e", padx=(0, 10))

        # Menu para selecao de modulacao
        self.ModulationLabel = Label(self.FrameConfig, text="Selecione a modulacao: ", font=("Calibri", "12"))
        self.ModulationLabel.grid(row=2, column=0, sticky="w", padx=(0, 10))

        self.ModulationSelect = OptionMenu(self.FrameConfig, self.ModulationChose, "")
        self.ModulationSelect.grid(row=2, column=1, sticky="e", padx=(0, 10))

        self.Label5G = Label(self.FrameConfig, text="5.2 GHz/5.4 GHz:", font=("Calibri","12"))
        self.Label5G.grid(row=3, column=0, columnspan=2, sticky="w", padx=(0, 10))

        self.Check5G = tk.Checkbutton(self.FrameConfig,variable=self.CheckState_5G)
        self.Check5G.grid(row=3, column=1, sticky="w")  


        self.SetFreqStartLabel = Label(self.FrameConfig, text="Informe a frequencia Inicial e Final da amostra: ", font=("Calibri","12"))
        self.SetFreqStartLabel.grid(row=4, column=0, columnspan=2, sticky="w", padx=(0, 10))
        
        self.StartFreqLabel = Label(self.FrameConfig, text="Freq.Inicial: ", font=("Calibri","12"))
        self.StartFreqLabel.grid(row=5, column=0, sticky="w", padx=(0,5))
      
        self.StartEntry = Entry(self.FrameConfig, font=("Arial", "10"), width= 7)
        self.StartEntry.grid(row=5, column=0,sticky="w", padx=(85,0))      
        
        self.StartMHz_Label = Label(self.FrameConfig, text="MHz", font=("Calibri","12"))
        self.StartMHz_Label.grid(row=5, column=0, sticky="w", padx=(127,0))

        self.FinalFreqLabel = Label(self.FrameConfig, text="Freq.Final: ", font=("Calibri","12"))
        self.FinalFreqLabel.grid(row=5, column=1, sticky="w", padx=(0,5))

        self.FinalEntry = Entry(self.FrameConfig, font=("Arial", "10"), width= 7)
        self.FinalEntry.grid(row=5, column=1,sticky="w", padx=(80,0))   
        
        self.FinalMHz_Label = Label(self.FrameConfig, text="MHz", font=("Calibri","12"))
        self.FinalMHz_Label.grid(row=5, column=1, sticky="w", padx=(127,0))
        
        self.PrintFileLabel = Label(self.FrameConfig, text="Selecione a pasta para os prints", font=("Calibri","12"))
        self.PrintFileLabel.grid(row=6, column=0, columnspan=2, sticky="w", padx=(0, 10))
        
        self.PathFileShow = Entry(self.FrameConfig, font=("Arial", "10"), width= 10)
        self.PathFileShow.grid(row=7, column=0, columnspan=2, sticky="we", padx=(0, 10))
        
        self.PathFileButton = Button(self.FrameConfig, text="Selecione a pasta", command=self.Print_screen_File, font=("Calibri", "10"), width=15)
        self.PathFileButton.grid(row=8, column=0, columnspan=2, sticky="we", padx=(0, 10))
        
    def LabelStartSequence(self):
        self.FrameStart = LabelFrame(text="Inicializar Teste", padx=10, pady=10)
        self.FrameStart.pack(side=TOP)          
        
        self.ButtonStart = Button(self.FrameStart, text="START", command=self.StartSequence, font=("Arial","16","bold"),width=25)
        self.ButtonStart.grid(row=0, column=0, sticky="we",padx=(5,5))

    def update_modulations(self, selected_technology):
        modulations = TechnologyModulations.get(selected_technology, [])
        # Limpar o menu existente
        menu = self.ModulationSelect["menu"]
        menu.delete(0, "end")
        # Adicionar novas opcoes de modulacao
        for modulation in modulations:
            menu.add_command(label=modulation, command=lambda value=modulation: self.ModulationChose.set(value))
        # Definir a modulacao padrao, se houver
        if modulations:
            self.ModulationChose.set(modulations[0])
        else:
            self.ModulationChose.set("")
        self.FrameConfig = LabelFrame(text="Configuracao para espurios", padx=10, pady=10)
        self.FrameConfig.pack(side=TOP)       

    def StartSequence(self):
        Status_5G = self.CheckState_5G.get()
        messagebox.showinfo("Inicio dos testes de Espurios","Selecione o canal inicial no seu ESE para Iniciar os testes")
        if Status_5G:
            self.execute_command(self.Command_Espur01_5G)
            time.sleep(5)
            self.execute_command(self.Command_Espur02_5G)
            messagebox.showinfo("Troca de selecao de canal","Selecione o canal final no seu ESE para continuar os testes")
            self.execute_command(self.Command_Espur03_5G)
            time.sleep(5)
            self.execute_command(self.Command_Espur04_5G)
            State_Print.clear()
            self.instr.go_to_local()
        else:
            self.execute_command(self.Command_Espur01)
            time.sleep(5)
            self.execute_command(self.Command_Espur02)
            messagebox.showinfo("Troca de selecao de canal","Selecione o canal final no seu ESE para continuar os testes")
            self.execute_command(self.Command_Espur03)
            time.sleep(5)
            self.execute_command(self.Command_Espur04)
            State_Print.clear()
            self.instr.go_to_local()

    def Command_Espur01(self):
        start_freq = int(self.StartEntry.get())
        start_freq_minus_10 = start_freq - 10 
        start_Mark2_str = str(start_freq_minus_10) #servira para o modo Marker
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 300 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 30 MHz",
            f"FREQ:STOP {self.StartEntry.get()} MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1:MAX",
            "CALC:DELT:X -10 MHz",
            "CALC:DELT:MAX:LEFT"
            ])
        State_Print.append(f"30-{self.StartEntry.get()}")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(0)
        
    def Command_Espur02(self):
        start_freq = int(self.StartEntry.get())
        start_freq_minus_10 = start_freq - 10 
        start_Mark2_str = str(start_freq_minus_10)
        start_freq_minus_100 = start_freq - 100  
        start_freq_minus_100_str = str(start_freq_minus_100)          
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 300 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:START {start_freq_minus_100_str} MHz",
            f"FREQ:STOP {self.StartEntry.get()} MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1:MAX",
            "CALC:DELT:X -10 MHz",
            "CALC:DELT:MAX:LEFT"
            ])     
        State_Print.append(f"{start_freq_minus_100_str}-{self.StartEntry.get()}")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(1)

    def Command_Espur03(self):
        Final_freq = int(self.FinalEntry.get())
        Final_freq_Plus_10 = Final_freq + 10          
        Final_freq_Plus_100 = Final_freq + 100  
        Final_freq_Plus_100_str = str(Final_freq_Plus_100)          
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 300 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:START {self.FinalEntry.get()} MHz",
            f"FREQ:STOP {Final_freq_Plus_100_str} MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1:MAX",
            "CALC:DELT:X 10 MHz",
            "CALC:DELT:MAX:RIGH"
            ])          
        State_Print.append(f"{self.FinalEntry.get()}-{Final_freq_Plus_100_str}")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(2)

    def Command_Espur04(self):
        Final_freq = int(self.FinalEntry.get())
        Final_freq_Plus_10 = Final_freq + 10           
        self.command_template([
                "*RST",
                "BAND 100 kHz",
                "BAND:VID 300 kHz",
                "DISP:WIND:TRAC:Y:RLEV 20dBm",
                "INP:ATT 40 DB",
                "DISP:WIND:TRAC:MODE MAXH",
                f"FREQ:START {self.FinalEntry.get()} MHz",
                "FREQ:STOP 18 GHz"
        ])      
        self.command_template([
            "CALC:MARK1:MAX",
            "CALC:DELT:X 10 MHz",
            "CALC:DELT:MAX:RIGH"
            ])           
        State_Print.append(f"{self.FinalEntry.get()}-18")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(3)

    def Command_Espur01_5G(self):
        start_freq = int(self.StartEntry.get())
        start_freq_minus_10 = start_freq - 10 
        start_Mark2_str = str(start_freq_minus_10) #servira para o modo Marker
        self.command_template([
            "*RST",
            "BAND 1 MHz",
            "BAND:VID 3 MHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 30 MHz",
            f"FREQ:STOP {self.StartEntry.get()} MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1:MAX",
            f"CALC:MARK2:X {start_Mark2_str} MHz",
            "CALC:MARK2:MAX:LEFT"
            ])
        State_Print.append(f"30-{self.StartEntry.get()}")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(0)

    def Command_Espur02_5G(self):
        start_freq = int(self.StartEntry.get())
        start_freq_minus_10 = start_freq - 10 
        start_Mark2_str = str(start_freq_minus_10)
        start_freq_minus_100 = start_freq - 100  
        start_freq_minus_100_str = str(start_freq_minus_100)          
        self.command_template([
            "*RST",
            "BAND 1 MHz",
            "BAND:VID 3 MHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:START {start_freq_minus_100_str} MHz",
            f"FREQ:STOP {self.StartEntry.get()} MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1:MAX",
            f"CALC:MARK2:X {start_Mark2_str} MHz",
            "CALC:MARK2:MAX:LEFT"
            ])     
        State_Print.append(f"{start_freq_minus_100_str}-{self.StartEntry.get()}")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(1)

    def Command_Espur03_5G(self):
        Final_freq = int(self.FinalEntry.get())
        Final_freq_Plus_10 = Final_freq + 10          
        Final_freq_Plus_100 = Final_freq + 100  
        Final_freq_Plus_100_str = str(Final_freq_Plus_100)          
        self.command_template([
            "*RST",
            "BAND 1 MHz",
            "BAND:VID 3 MHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:START {self.FinalEntry.get()} MHz",
            f"FREQ:STOP {Final_freq_Plus_100_str} MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1:MAX",
            f"CALC:MARK2:X {Final_freq_Plus_10} MHz",
            "CALC:MARK2:MAX:RIGH"
            ])          
        State_Print.append(f"{self.FinalEntry.get()}-{Final_freq_Plus_100_str}")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(2)

    def Command_Espur04_5G(self):
        Final_freq = int(self.FinalEntry.get())
        Final_freq_Plus_10 = Final_freq + 10           
        self.command_template([
                "*RST",
                "BAND 1 MHz",
                "BAND:VID 3 MHz",
                "DISP:WIND:TRAC:Y:RLEV 20dBm",
                "INP:ATT 40 DB",
                "DISP:WIND:TRAC:MODE MAXH",
                f"FREQ:START {self.FinalEntry.get()} MHz",
                "FREQ:STOP 18 GHz"
        ])      
        self.command_template([
            "CALC:MARK1:MAX",
            f"CALC:MARK2:X {Final_freq_Plus_10} MHz",
            "CALC:MARK2:MAX:RIGH"
            ])           
        State_Print.append(f"{self.FinalEntry.get()}-18")
        print(State_Print)
        time.sleep(2)
        self.Print_Screen_Func(3)





    def execute_command(self, command_function):
        try:
            command_function()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def command_template(self, commands):
        for command in commands:
            self.instr.write_str(command)
        #self.instr.go_to_local()

    def Print_screen_File(self):
        default_dir = r"C:\\"        

        if messagebox.askyesno("Escolha do Diretorio", "Deseja escolher o local para salvar o print?"):
          self.save_dir = filedialog.askdirectory(title="Selecione o diretorio para salvar o print")
          if self.save_dir:
            self.PathFileShow.delete(0, END)
            self.PathFileShow.insert(0, self.save_dir)
          if not self.save_dir:
              messagebox.showerror("Erro", "Nenhum diretorio selecionado. Cancelando operacao.")
              return
        else:
          self.save_dir = default_dir


    def Print_Screen_Func(self,IndexPrint):
        try:
            if self.ip_val:  # Verifica se ha um IP configurado
                try:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
                    Protocolo = self.ProtocolEntry.get()
                    ModulationGet = self.ModulationChose.get()
                    self.save_path = os.path.join(self.save_dir, f"ESP_{ModulationGet} {State_Print[IndexPrint]}_{Protocolo}_{timestamp}.png")                    
                    # Conectar ao FSMR
                    instr = RsInstrument(f'TCPIP::{self.ip_val}::INSTR', True, False)
            
                    # Enviar comando de captura de tela (SCPI generico, adaptar se necessario)
                    instr.write_str('HCOP:DEST "MMEM"')  # Enviar print para a memoria interna
                    instr.write_str(f'MMEM:NAME "C:\\Temp\\screen.bmp"')  # Nome temporario no FSMR
                    instr.write_str('HCOP:IMM')  # Capturar a tela imediatamente
            
                    # Baixar o arquivo do FSMR
                    instr.query_bin_block_to_file('MMEM:DATA? "C:\\Temp\\screen.bmp"', self.save_path)
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao salvar o print.\n{e}")
                finally:
                    instr.close()
            else:
                messagebox.showerror("Erro", "IP nao configurado. Conecte-se a um instrumento primeiro.")
        except :
            messagebox.showerror("Erro", "IP nao configurado. Conecte-se a um instrumento primeiro.")




def main():
    app = MainProgram()  # Apenas cria a MainProgram
    app.mainloop()

if __name__ == "__main__":
    main()
