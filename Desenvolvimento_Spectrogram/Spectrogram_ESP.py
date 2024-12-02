import time
from tkinter import *
import os
import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu, StringVar
from RsInstrument.RsInstrument import RsInstrument

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
        
        self.TechnologyLabel = Label(self.FrameConfig, text="Selecione a tecnologia: ", font=("Calibri", "12"))
        self.TechnologyLabel.grid(row=1, column=0, sticky="w", padx=(0, 10))

        self.TechnologySelect = OptionMenu(self.FrameConfig, self.TechnologyChose, *TechnologyModulations.keys(), command=self.update_modulations)
        self.TechnologySelect.grid(row=1, column=1, sticky="e", padx=(0, 10))

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

    def StartSequence(self):
        Status_5G = self.CheckState_5G.get()
        FirthFreq = self.StartEntry.get()
        LestFreq = self.FinalEntry.get()
        try:
            messagebox.showinfo("Inicio dos testes de Espurios","Selecione o canal inicial no seu ESE para Iniciar os testes")
            for stage in range(4):
                if stage == 2:
                    messagebox.showinfo("Troca de selecao de canal","Selecione o canal final no seu ESE para continuar os testes")
                self.Command_Espurios(stage, Status_5G, FirthFreq, LestFreq)
            self.instr.go_to_local()
            messagebox.showinfo ("Operacao Concluida!","Testes concluido, prints salvos na pasta!")
        except Exception as e:
            messagebox.showerror("Erro ao executar",f"Falha na execucao do processo: \n{e}")

    def ModulationSelector(self):
        modulation = self.ModulationChose.get()
        Bandwidth_MHz = 10
        if "40" in modulation:
            Bandwidth_MHz = 30 # (40/2)+10 = 30 MHz
        elif "80" in modulation:
            Bandwidth_MHz = 50 # (80/2)+10 = 50 MHz
        elif "160" in modulation:
            Bandwidth_MHz = 90 # (160/2)+10 = 90 MHz
        elif "320" in modulation: 
            Bandwidth_MHz = 170 # (320/2)+10 = 170 MHz
        elif "GFSK" or "8DQPSK" or "PI-4DQPSK" or "BLE 1M" or "DBPSK" or "O-QPSK" in modulation:
            Bandwidth_MHz = 10 # 10 MHz para larguras de 1 MHz
        else:
            Bandwidth_MHz = 20 # para os demais, espaco de ate 20 MHZ        
        return Bandwidth_MHz
    
    def Command_Espurios(self,SelectStep,Status_5G,FirthFreq, LestFreq): # a funcao esta imensa, vou tentar pensar em como reduzir isso mais tarde. terao outros acrecimo // Olhar nota no inicio do codigo
        Final_freq = int(LestFreq)
        start_freq = int(FirthFreq)
        if Status_5G:
            RBW = "BAND 1 MHz"
            VBW = "BAND:VID 3 MHz"
            MarkDelt = "MARK2"
            if SelectStep == 0 or SelectStep ==  1:
                Position = f"{str(start_freq - self.ModulationSelector())}"
            elif SelectStep == 2 or SelectStep ==  3:
                Position = f"{str(Final_freq + self.ModulationSelector())}"
        else:
            RBW = "BAND 100 kHz"
            VBW = "BAND:VID 300 kHz"
            MarkDelt = "DELT"
            if SelectStep == 0 or SelectStep ==  1:
                Position = f"-{str(self.ModulationSelector())}"              
            elif SelectStep == 2 or SelectStep ==  3:
                Position = f"{str(self.ModulationSelector())}"
        if SelectStep == 0:
            Stepper_Start = "FREQ:START 30 MHz"
            Stepper_Stop = f"FREQ:STOP {FirthFreq} MHz"
            Command_Marker_Start = f"CALC:{MarkDelt}:X {Position} MHz"
            Command_Marker_Finish = f"CALC:{MarkDelt}:MAX:LEFT"
            Name_Print = f"30-{FirthFreq}"
        elif SelectStep == 1:
            Stepper_Start = f"FREQ:START {str(start_freq - 100)} MHz"
            Stepper_Stop = f"FREQ:STOP {FirthFreq} MHz"
            Command_Marker_Start = f"CALC:{MarkDelt}:X {Position} MHz"
            Command_Marker_Finish = f"CALC:{MarkDelt}:MAX:LEFT"
            Name_Print = f"{str(start_freq - 100)}-{FirthFreq}"
        elif SelectStep == 2:
            Stepper_Start = f"FREQ:START {LestFreq} MHz"
            Stepper_Stop  = f"FREQ:STOP {str(Final_freq + 100)} MHz"  
            Command_Marker_Start = f"CALC:{MarkDelt}:X {Position} MHz"
            Command_Marker_Finish = f"CALC:{MarkDelt}:MAX:RIGH"
            Name_Print = f"{LestFreq}-{str(Final_freq + 100)}"
        elif SelectStep == 3:
            Stepper_Start = f"FREQ:START {LestFreq} MHz"
            Stepper_Stop  = f"FREQ:STOP 18 GHz"
            Command_Marker_Start = f"CALC:{MarkDelt}:X {Position} MHz"
            Command_Marker_Finish = f"CALC:{MarkDelt}:MAX:RIGH"
            Name_Print = f"{LestFreq}-18"
        self.command_template([
            "*RST",
            f"{RBW}",
            f"{VBW}",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"{Stepper_Start}",
            f"{Stepper_Stop}"
        ])        
        time.sleep(5)
        self.command_template(["CALC:MARK1:MAX",f"{Command_Marker_Start}",f"{Command_Marker_Finish}"])
        self.Print_Screen_Func(Name_Print)
        
    def command_template(self, commands):
        for command in commands:
            self.instr.write_str(command)
            
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
            if self.ip_val:
                try:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
                    Protocolo = self.ProtocolEntry.get()
                    ModulationGet = self.ModulationChose.get()
                    self.save_path = os.path.join(self.save_dir, f"ESP_{ModulationGet} {IndexPrint}_{Protocolo}_{timestamp}.png")                    
                    instr = RsInstrument(f'TCPIP::{self.ip_val}::INSTR', True, False)# Enviar comando de captura de tela (SCPI generico, adaptar se necessario)
                    instr.write_str('HCOP:DEST "MMEM"')  # Enviar print para a memoria interna
                    instr.write_str(f'MMEM:NAME "C:\\Temp\\screen.bmp"')  # Nome temporario no FSMR
                    instr.write_str('HCOP:IMM')  # Capturar a tela imediatamente
                    instr.query_bin_block_to_file('MMEM:DATA? "C:\\Temp\\screen.bmp"', self.save_path)# Baixar o arquivo do FSMR
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao salvar o print.\n{e}")
                finally:
                    instr.close()
            else:
                messagebox.showerror("Erro", "IP nao configurado. Conecte-se a um instrumento primeiro.")
        except :
            messagebox.showerror("Erro", "IP nao configurado. Conecte-se a um instrumento primeiro.")

def main():
    app = MainProgram() 
    app.mainloop()

if __name__ == "__main__":
    main()
