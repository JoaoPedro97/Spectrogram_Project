# -*- coding: utf-8 -*-
from ast import Return
from asyncio.windows_events import NULL
from email.mime import nonmultipart
import time
from pickle import PROTO
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import os
from tkinter import filedialog
from logging import root
from tkinter import ttk
from token import NAME
import serial
import serial.tools.list_ports
from RsInstrument.RsInstrument import RsInstrument



commands = {
    "StartFreqGFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x02, 0x00, 0x0A, 0x00]),
    "MidleFreqGFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x28, 0x02, 0x00, 0x0A, 0x00]),
    "FinalFreqGFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x4E, 0x02, 0x00, 0x0A, 0x00]),
    
    "EspacamentoLEFT_GFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x27, 0x02, 0x00, 0x0A, 0x00]),
    "EspacamentoRIGH_GFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x29, 0x02, 0x00, 0x0A, 0x00]),

    "HoppingGFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x02, 0x00, 0x0A, 0x01]),
    
    "StartFreq4PID": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x05, 0x00, 0x0A, 0x00]),
    "MidleFreq4PID": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x28, 0x05, 0x00, 0x0A, 0x00]),
    "FinalFreq4PID": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x4E, 0x05, 0x00, 0x0A, 0x00]),
    
    "HoppingGFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x05, 0x00, 0x0A, 0x01]),

    "StartFreq8DPSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x08, 0x00, 0x0A, 0x00]),
    "MidleFreq8DPSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x28, 0x08, 0x00, 0x0A, 0x00]),
    "FinalFreq8DPSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x4E, 0x08, 0x00, 0x0A, 0x00]),
    
    "HoppingGFSK": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x08, 0x00, 0x0A, 0x01])
    }



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
        self.geometry("450x800")
        self.title("Bluetooth destroyer. Monster edition")

        self.create_widgets_TestConnection()
        #elf.create_Ensaios_Bluetooth()
        self.Interface_Conections_COM()
        self.create_Printscreen()
        self.StartSequence()

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

    def Interface_Conections_COM(self):
        self.Container_COM = LabelFrame(text="ESE_Connection", padx=10, pady=10)
        self.Container_COM.pack(side=TOP)

        tk.Label(self.Container_COM, text="Porta COM:").pack(side=tk.LEFT, padx=5)
        self.combo_porta = ttk.Combobox(self.Container_COM, values=self.listar_portas(), width=10)
        self.combo_porta.pack(side=tk.LEFT, padx=5)
        self.combo_porta.set( "Selecione")       

        tk.Label(self.Container_COM, text="Baud Rate:").pack(side=tk.LEFT, padx=5)
        self.combo_baudrate = ttk.Combobox(self.Container_COM, values=["9600", "19200", "38400", "57600", "115200"], width=10)
        self.combo_baudrate.pack(side=tk.LEFT, padx=5)
        self.combo_baudrate.set("115200")

        self.btn_conectar = tk.Button(self.Container_COM, text="Conectar", command=self.conectar)
        self.btn_conectar.pack(side=tk.LEFT, padx=5)

    def StartSequence(self):
        self.Container_Start = LabelFrame(text="Inicio dos testes (FULL DEVICE)", padx=10, pady=10)
        self.Container_Start.pack(side=TOP)     
        
        self.Start_Destroyer = tk.Button(self.Container_Start, text="Start All tests",font=("Arial","12","bold"), command=self.StartAll, width=40)
        self.Start_Destroyer.pack(side=tk.LEFT, padx=5)

    def StartAll(self):
        try:
            if  self.ip_val:
                if self.Print_Save:
                    messagebox.showinfo("Iniciando testes!", f"Inicio dos testes versao BETA")
                    self.MasterMind()
                else:
                    messagebox.showerror("Pasta nao declarada","Indique a pasta para salvar os arquivos")
            else:
                messagebox.showerror("IP nao declarado","indique o IP do Analisador de espectro a ser utilizado")
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel concluir o processo \n {e}")

    def listar_portas(self):
        self.ports = serial.tools.list_ports.comports()
        return [port.device for port in self.ports]
    
    def MasterMind(self):
        ser = self.configure_uart(self.combo_porta.get(), int(self.combo_baudrate.get()))
        if ser:
            self.Inicio_Espacamento("2442")
            print("[FLEG] - Setou Espacamento") # Aumentar a complexidade dessa etapa
            self.send_command(ser, commands["MidleFreqGFSK"])
            self.send_command(ser, commands["EspacamentoLEFT_GFSK"])
            time.sleep(1)
            self.send_command(ser, commands["EspacamentoRIGH_GFSK"])
            print("[FLEG] aqui eu teria que fazer a funcao pra espacamento")
            time.sleep(5)
            self.Print_Screen_Func("GFSK")
            print("[FLEG] Tirou print aqui e passou pra proxima")
            time.sleep(1)
            self.send_command(ser, commands["StartFreqGFSK"])
            time.sleep(2)
            self.Inicio_Largura20dB("2402")
            time.sleep(2)
            self.send_command(ser, commands["MidleFreqGFSK"])
            time.sleep(1)
            self.Inicio_Largura20dB("2442")
            self.Print_Screen_Func("GFSK")
            time.sleep(2)
            self.send_command(ser, commands["FinalFreqGFSK"])
            time.sleep(1)
            self.Inicio_Largura20dB("2480")
            time.sleep(2)
            self.send_command(ser, commands["StartFreqGFSK"])
            time.sleep(2)
            self.Inicio_Potencia("2402")
            time.sleep(2)
            self.send_command(ser, commands["MidleFreqGFSK"])
            time.sleep(1)
            self.Inicio_Potencia("2442")
            self.Print_Screen_Func("GFSK")
            time.sleep(2)
            self.send_command(ser, commands["FinalFreqGFSK"])
            time.sleep(1)
            self.Inicio_Potencia("2480")

            print("Fim do teste de exposicao")
        else:
            print("FUCK")
            

    def configure_uart(self,port, baudrate=115200, timeout=1):
        """
        Configura a porta UART com os parametros especificados.
        """
        try:
            ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            print(f"[INFO] Porta {port} aberta com sucesso!")
            return ser
        except Exception as e:
            print(f"[ERRO] Nao foi possivel abrir a porta {port}: {e}")
            return None
        self.close_uart(ser)





    def conectar(self):
        global ser
        porta = self.combo_porta.get()
        baudrate = int(self.combo_baudrate.get())
        try:
            ser = serial.Serial(porta, baudrate=baudrate, timeout=1)
            messagebox.showinfo("Sucesso", f"Conectado a porta {porta} com baud rate {baudrate}")
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel abrir a porta {porta}: {e}")
        self.close_uart(ser)






    def send_command(self,ser, command):
        """
        Envia um comando HCI pela UART e aguarda a resposta.
        """
        try:
            print(f"[ENVIO] Comando: {command.hex()}")
            ser.write(command)  # Envia o comando
            time.sleep(0.1)     # Pequeno atraso para garantir a resposta
            response = ser.read(ser.in_waiting or 100)  # Le a resposta disponivel
            if response:
                print(f"[RESPOSTA] -  {response.hex()}")
            else:
                print("[RESPOSTA] Nenhuma resposta recebida.")
            return response
        except Exception as e:
            print(f"[ERRO] Falha ao enviar o comando: {e}")
            return None

    def close_uart(self,ser):
        """
        Fecha a porta UART de maneira segura.
        """
        if ser and ser.is_open:
            ser.close()
            print("[INFO] Porta UART fechada.")


    def command_template(self, commands):
        for command in commands:
            self.instr.write_str(command)
        self.instr.go_to_local()

    def Command_Espacamento(self,FREQ):
        self.command_template([
            "*RST",
            "BAND 100kHz",
            "BAND:VID 300kHz",
            "DISP:WIND:TRAC:Y:RLEV 10dBm",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:CENT {FREQ} MHz",
            "FREQ:SPAN 3 MHz"
        ])

    def Command_Largura20dB(self,FREQ):
        # Configuracoes e inicializacoes
        self.command_template([
            "*RST",  # Reseta o instrumento
            "DISP:WIND:TRAC:MODE WRIT",  # Define modo de escrita na tela
            "INIT:CONT ON",  # Desativa trigger continuo
            "BAND 100kHz",  # Configura RBW para 100 kHz
            "BAND:VID 300kHz",  # Configura VBW para 300 kHz
            "DISP:WIND:TRAC:Y:RLEV 10dBm",  # Ajusta o nivel de referencia
            f"FREQ:CENT {FREQ} MHz",  # Ajusta frequencia central
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

    def Command_Potencia(self,FREQ):
        self.command_template([
            "*RST",
            "BAND 1 MHz",
            "BAND:VID 3 MHz",
            "DISP:WIND:TRAC:Y:RLEV 20dBm",
            "INP:ATT 40 DB",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:CENT {FREQ} MHz",
            "FREQ:SPAN 3 MHz"
        ])
        time.sleep(5)
        self.command_template([
            "CALC:MARK1 ON",
            "CALC:MARK:MAX"
            ])
        result = self.instr.query("CALC:MARK1:Y?")  # Captura o valor do instrumento como string
        try:
            result_float = float(result)  # Converte o resultado para um numero de ponto flutuante
            rounded_result = round(result_float, 2)  # Arredonda para 2 casas decimais
            return rounded_result
        except ValueError:
            # Caso o resultado nao possa ser convertido (erro inesperado), retorna uma mensagem padrao
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

    def Inicio_Espacamento(self,FREQ):
        self.execute_command(self.Command_Espacamento(FREQ))
        self.selection_Name = Test_Name[0]

    def Inicio_Largura20dB(self,FREQ):
        try:
            # Chama a funcao que realiza os comandos e captura o resultado
            largura = self.Command_Largura20dB(FREQ)
            # Exibe o resultado em uma messagebox
            #messagebox.showinfo("Resultado da Largura de Banda", f"A largura de banda a 20 dB e: {largura} Hz")
            print(f"[FLEG] Feito a largura, retorno do valor: {largura}")
        except Exception as e:
            # Trata erros e exibe mensagem na messagebox
            messagebox.showerror("Erro", f"Erro ao calcular a largura de banda: {e}")
        self.selection_Name = Test_Name[1]

    def Inicio_Potencia(self,FREQ):
        try:
            # Chama a funcao que realiza os comandos e captura o resultado
            Potencia = self.Command_Potencia(FREQ)
            
            # Exibe o resultado em uma messagebox
            #messagebox.showinfo("Potencia medida", f"A potencia de medida: {Potencia} dBm")
            print(f"[FLEG] Feito a potencia, retorno do valor: {Potencia}")
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
        
        #self.Modulation_Seting = tk.OptionMenu(self.Pacote01,self.Pre_Select_Modulation,*Modulation_Bluetooth)
        #self.Modulation_Seting.grid(row=1, column=1, sticky="e", padx=(0, 10))

        self.LocFile_Button = Button(self.Pacote01, text="Escolher local", command=self.Print_screen_File, font=("Calibri", "10"), width=15)
        self.LocFile_Button.grid(row=2, column=0, sticky="w", padx=(0, 10))

        #self.Print_Button = Button(self.Pacote01, text="PrintScreen", command=self.Print_Screen_Func, font=("Calibri", "10"), width=15)
        #self.Print_Button.grid(row=2, column=1, sticky="e", padx=(0, 10))
       
      


    def Print_screen_File(self):
        default_dir = r"C:\\"        

        if messagebox.askyesno("Escolha do Diretorio", "Deseja escolher o local para salvar o print?"):
          self.save_dir = filedialog.askdirectory(title="Selecione o diretorio para salvar o print")
          if self.save_dir:
            self.EndEntry.delete(0, END)
            self.EndEntry.insert(0, self.save_dir)
            self.Print_Save = True
          if not self.save_dir:
              messagebox.showerror("Erro", "Nenhum diretorio selecionado. Cancelando operacao.")
              return
        else:
          self.save_dir = default_dir


          
    def Print_Screen_Func(self,ModulationGet):
        try:
            if self.ip_val:  # Verifica se ha um IP configurado
                try:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
                    Protocolo = self.ProtocolEntry.get()
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
                    #messagebox.showinfo("Sucesso", f"Print salvo com sucesso em:\n{self.save_path}")
                    
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
