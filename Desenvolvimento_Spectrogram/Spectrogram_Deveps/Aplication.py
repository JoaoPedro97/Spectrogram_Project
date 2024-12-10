from ast import Return
import time
from pickle import PROTO
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import os
from tkinter import filedialog
from logging import root
from token import NAME
from RsInstrument.RsInstrument import RsInstrument


Test_Name = ["2442 Separacao Canais de Salto",
             "2442 Largura 20db",
             "2442 Potencia_de_pico_maxima",
             "2400 2440.5 numero de Canais de Salto",
             "2440.5 2483.5 numero de Canais de Salto",
             "2442 NumeroDeOcupacoes",
             "2442 TempoDeOcupacao",
             "ESP_30_2402",
             "ESP_2302_2402",
             "ESP_2480_2580",
             "ESP_2480_18"]

Modulation_Bluetooth = ["GFSK",
                        "8DQPSK",
                        "PI-4DQPSK"]

class MainProgram(tk.Tk):  # Herdando de Tk em vez de Toplevel
    def __init__(self):
        super().__init__()  # Inicializa o Tk
        self.geometry("500x800")
        self.title("Spectrogram Alfa")

        self.create_widgets_TestConnection()
        self.create_Ensaios_Bluetooth()
        self.create_Printscreen()

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

    def create_Ensaios_Bluetooth(self):
        self.EnsaiosBluetooth = LabelFrame(text="Ensaios de Bluetooth - Presets", padx=10, pady=10)
        self.EnsaiosBluetooth.pack(side=TOP)

        ensaios = [
            ("Espacamento", self.Inicio_Espacamento, "Freq", "EspacamentoEntry", "MHz"),
            ("Largura de faixa a 20 dB", self.Inicio_Largura20dB, "Freq", "LarguraEntry", "MHz"),
            ("Potencia de pico maxima de saida", self.Inicio_Potencia, "Freq", "PotenciaEntry", "MHz"),
            ("Numero de frequencias de salto", self.Inicio_NumeroFreq01, " 2.400 GHz a 2.4405 GHz ", None, "01"),
            ("Numero de frequencias de salto", self.Inicio_NumeroFreq02, " 2.4405 GHz a 2.4835 GHz ", None, "02"),
            ("Numero de utilizacoes", self.Inicio_Num_Util, " 2.442 ", None, "GHz"),
            ("Tempo de duracao de um Slot", self.Inicio_Temp_Dur, " 2.442 ", None, "GHz"),
            ("Espurios 30 MHz a 2.402 GHz", self.Inicio_Espur01, None, None, None),
            ("Espurios 2.302 GHz a 2.402 GHz", self.Inicio_Espur02, None, None, None),
            ("Espurios 2.480 GHz a 2.580 GHz", self.Inicio_Espur03, None, None, None),
            ("Espurios 2.480 GHz a 18 GHz", self.Inicio_Espur04, None, None, None)
        ]

        for ensaio in ensaios:
            self.add_ensaio(*ensaio)

    def add_ensaio(self, text, command, label_text, entry_attr, unit_text):
        frame = Frame(self.EnsaiosBluetooth)
        frame.pack(anchor="w", pady=5)

        button = Button(frame, text=text, command=command, width=28)
        button.pack(side=LEFT)

        if label_text:
            label = Label(frame, text=label_text)
            label.pack(side=LEFT)

        if entry_attr:
            entry = Entry(frame)
            setattr(self, entry_attr, entry)
            entry.pack(side=LEFT)

        if unit_text:
            unit = Label(frame, text=unit_text)
            unit.pack(side=LEFT)

    def command_template(self, commands):
        for command in commands:
            self.instr.write_str(command)
        self.instr.go_to_local()

    def Command_Espacamento(self):
        self.command_template([
            "*RST",
            "BAND 100kHz",
            "BAND:VID 300kHz",
            "DISP:WIND:TRAC:Y:RLEV 10dBm",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:CENT {self.EspacamentoEntry.get()} MHz",
            "FREQ:SPAN 3 MHz"
        ])

    def Command_Largura20dB(self):
        # Configuracoes e inicializacoes
        self.command_template([
            "*RST",  # Reseta o instrumento
            "DISP:WIND:TRAC:MODE WRIT",  # Define modo de escrita na tela
            "INIT:CONT ON",  # Desativa trigger continuo
            "BAND 100kHz",  # Configura RBW para 100 kHz
            "BAND:VID 300kHz",  # Configura VBW para 300 kHz
            "DISP:WIND:TRAC:Y:RLEV 10dBm",  # Ajusta o nivel de referencia
            f"FREQ:CENT {self.LarguraEntry.get()} MHz",  # Ajusta frequencia central
            "FREQ:SPAN 3 MHz",  # Define o span como 3 MHz
            "DISP:WIND:TRAC:MODE MAXH",  # Ativa retencao de maximos
            "INIT; *WAI"  # Inicia varredura e aguarda
        ])
        time.sleep(5)
        # Configura NdB Down
        self.command_template([
            "CALC:MARK1:FUNC:NDBD:STAT ON",
            "CALC:MARK1:FUNC:NDBD 20 dB"
        ])
        
        # Captura o valor da largura de banda
        result = self.instr.query("CALC:MARK1:FUNC:NDBD:RES?")
        return result

    def Command_Potencia(self):
        self.command_template([
            "*RST",
            "BAND 1 MHz",
            "BAND:VID 3 MHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:CENT {self.PotenciaEntry.get()} MHz",
            "FREQ:SPAN 3 MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1 ON",
            "CALC:MARK:MAX"
            ])
        result = self.instr.query("CALC:MARK1:Y?")  # Captura o valor do instrumento como string
        try:
            result_float = float(result)  # Converte o resultado para um número de ponto flutuante
            rounded_result = round(result_float, 2)  # Arredonda para 2 casas decimais
            return rounded_result
        except ValueError:
            # Caso o resultado não possa ser convertido (erro inesperado), retorna uma mensagem padrão
            return "Erro no resultado"

    def Command_NumeroFreq01(self):
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 100 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 2400 MHz",
            "FREQ:STOP 2440.5 MHz"
        ])

    def Command_NumeroFreq02(self):
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 100 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 2440.5 MHz",
            "FREQ:STOP 2483.5 MHz"
        ])

    def Command_Num_Util(self):
        self.command_template([
            "FREQ:SPAN 0",
            "BAND 300 kHz",
            "BAND:VID 300 kHz",
            "SWE:TIME 1 s",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 2442 MHz",
            "INIT:CONT OFF",
            "INIT:IMM"
        ])

    def Command_Temp_Dur(self):
        self.command_template([
            "FREQ:SPAN 0",
            "BAND 1 MHz",
            "BAND:VID 3 MHz",
            "SWE:TIME 0.02 s",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 2442 MHz",
            "INIT:CONT OFF",
            "INIT:IMM"
        ])

    def Command_Espur01(self):
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 300 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 30 MHz",
            "FREQ:STOP 2402 MHz"
        ])

    def Command_Espur02(self):
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 300 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 2302 MHz",
            "FREQ:STOP 2402 MHz"
        ])

    def Command_Espur03(self):
        self.command_template([
            "*RST",
            "BAND 100 kHz",
            "BAND:VID 300 kHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            "FREQ:START 2480 MHz",
            "FREQ:STOP 2580 MHz"
        ])

    def Command_Espur04(self):
        self.command_template([
                "*RST",
                "BAND 100 kHz",
                "BAND:VID 300 kHz",
                "DISP:WIND:TRAC:Y:RLEV 20dBm",
                "INP:ATT 40 DB",
                "DISP:WIND:TRAC:MODE MAXH",
                "FREQ:START 2480 MHz",
                "FREQ:STOP 18 GHz"
        ])

    def execute_command(self, command_function):
        try:
            command_function()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Espacamento(self):
        self.execute_command(self.Command_Espacamento)
        self.selection_Name = Test_Name[0]

    def Inicio_Largura20dB(self):
        try:
            # Chama a funcao que realiza os comandos e captura o resultado
            largura = self.Command_Largura20dB()
            
            # Exibe o resultado em uma messagebox
            messagebox.showinfo("Resultado da Largura de Banda", f"A largura de banda a 20 dB e: {largura} Hz")
        except Exception as e:
            # Trata erros e exibe mensagem na messagebox
            messagebox.showerror("Erro", f"Erro ao calcular a largura de banda: {e}")
        self.selection_Name = Test_Name[1]

    def Inicio_Potencia(self):
        try:
            # Chama a funcao que realiza os comandos e captura o resultado
            Potencia = self.Command_Potencia()
            
            # Exibe o resultado em uma messagebox
            messagebox.showinfo("Potencia medida", f"A potencia de medida: {Potencia} dBm")
        except Exception as e:
            # Trata erros e exibe mensagem na messagebox
            messagebox.showerror("Erro", f"Erro ao calcular a Potencia de pico: {e}")
        self.selection_Name = Test_Name[2]
        
    def Inicio_NumeroFreq01(self):
        self.execute_command(self.Command_NumeroFreq01)
        self.selection_Name = Test_Name[3]

    def Inicio_NumeroFreq02(self):
        self.execute_command(self.Command_NumeroFreq02)
        self.selection_Name = Test_Name[4]

    def Inicio_Num_Util(self):
        self.execute_command(self.Command_Num_Util)
        self.selection_Name = Test_Name[5]

    def Inicio_Temp_Dur(self):
        self.execute_command(self.Command_Temp_Dur)
        self.selection_Name = Test_Name[6]

    def Inicio_Espur01(self):
        self.execute_command(self.Command_Espur01)
        self.selection_Name = Test_Name[7]

    def Inicio_Espur02(self):
        self.execute_command(self.Command_Espur02)
        self.selection_Name = Test_Name[8]

    def Inicio_Espur03(self):
        self.execute_command(self.Command_Espur03)
        self.selection_Name = Test_Name[9]

    def Inicio_Espur04(self):
        self.execute_command(self.Command_Espur04)
        self.selection_Name = Test_Name[10]

    def create_Printscreen(self):
        
        self.Pre_Select_Modulation = tk.StringVar(self)
        self.Pre_Select_Modulation.set(Modulation_Bluetooth[0]) 
        
        self.Container_Print = LabelFrame(text="PrintScreen Options", padx=10, pady=10)
        self.Container_Print.pack(side=TOP)
        
        self.Pacote01 = Frame(self.Container_Print)
        self.Pacote01.pack(side=TOP)
        
        self.EndLabel = Label(self.Pacote01, text="Endereco da pasta", font=("Calibri", "12"))
        self.EndLabel.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.EndEntry = Entry(self.Pacote01, font=("Arial", "10"), width=35)
        self.EndEntry.grid(row=0, column=1, sticky="w", padx=(0, 10))
        
        self.ProtocolLabel = Label(self.Pacote01, text="Protocolo:", font=("Calibri", "12"))
        self.ProtocolLabel.grid(row=1, column=0, sticky="w", padx=(0, 10))
        
        self.ProtocolEntry = Entry(self.Pacote01, font=("Arial", "10"), width=25)
        self.ProtocolEntry.grid(row=1, column=1, sticky="w", padx=(0, 10))
        
        self.Modulation_Seting = tk.OptionMenu(self.Pacote01,self.Pre_Select_Modulation,*Modulation_Bluetooth)
        self.Modulation_Seting.grid(row=1, column=1, sticky="e", padx=(0, 10))

        self.LocFile_Button = Button(self.Pacote01, text="Escolher local", command=self.Print_screen_File, font=("Calibri", "10"), width=15)
        self.LocFile_Button.grid(row=2, column=0, sticky="w", padx=(0, 10))

        self.Print_Button = Button(self.Pacote01, text="PrintScreen", command=self.Print_Screen_Func, font=("Calibri", "10"), width=15)
        self.Print_Button.grid(row=2, column=1, sticky="e", padx=(0, 10))
       
      


    def Print_screen_File(self):
        default_dir = r"C:\\"        

        if messagebox.askyesno("Escolha do Diretorio", "Deseja escolher o local para salvar o print?"):
          self.save_dir = filedialog.askdirectory(title="Selecione o diretorio para salvar o print")
          if self.save_dir:
            self.EndEntry.delete(0, END)
            self.EndEntry.insert(0, self.save_dir)
          if not self.save_dir:
              messagebox.showerror("Erro", "Nenhum diretorio selecionado. Cancelando operacao.")
              return
        else:
          self.save_dir = default_dir


          
    def Print_Screen_Func(self):
        try:
            if self.ip_val:  # Verifica se ha um IP configurado
                try:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
                    Protocolo = self.ProtocolEntry.get()
                    ModulationGet = self.Pre_Select_Modulation  .get()
                    self.save_path = os.path.join(self.save_dir, f"{ModulationGet} {self.selection_Name}_{Protocolo}_{timestamp}.png")                    
                    # Conectar ao FSMR
                    instr = RsInstrument(f'TCPIP::{self.ip_val}::INSTR', True, False)
            
                    # Enviar comando de captura de tela (SCPI generico, adaptar se necessario)
                    instr.write_str('HCOP:DEST "MMEM"')  # Enviar print para a memoria interna
                    instr.write_str(f'MMEM:NAME "C:\\Temp\\screen.bmp"')  # Nome temporario no FSMR
                    instr.write_str('HCOP:IMM')  # Capturar a tela imediatamente
            
                    # Baixar o arquivo do FSMR
                    instr.query_bin_block_to_file('MMEM:DATA? "C:\\Temp\\screen.bmp"', self.save_path)
            
                    # Notificar o sucesso
                    messagebox.showinfo("Sucesso", f"Print salvo com sucesso em:\n{self.save_path}")
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
