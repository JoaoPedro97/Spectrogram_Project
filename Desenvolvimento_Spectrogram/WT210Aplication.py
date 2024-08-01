from ipaddress import collapse_addresses
from optparse import Option
from tkinter import *
from tkinter import messagebox
from tkinter import messagebox, scrolledtext
import tkinter as tk
from tkinter.ttk import Labelframe
from turtle import st
from urllib import response
from RsInstrument.Internal.Core import WaitForOpcMode
import pyvisa
import time
import csv
from datetime import datetime, timedelta

global_GPIB_COM = ["0","1","2","3","4","5","6","7","8","9"]
global_Escala_Corrente = ["0.5","1","2","5","10","20","AUTO"]
global_Escala_Tensao = ["15","30","60","150","300","600","AUTO"]

class MainProgram(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry("750x650")
        self.master.title("WT210 Application Measurement")

        self.Containers()
        self.pack()

    def Containers(self):
        self.Linha1 = Frame(self)
        self.Linha1.pack(side=TOP)

        self.Linha2 = Frame(self)
        self.Linha2.pack(side=TOP)
        
        self.Linha3 = Frame(self)
        self.Linha3.pack(side=TOP)
        
        self.ConnectionGPIB_Frame()
        self.Escale_Frame()
        self.Set_Measurement_Frame()
        self.Start_Frame()
        self.Log_Frame()
        
    def ConnectionGPIB_Frame(self):
        self.Pre_select_GPIB_Addres = StringVar(self)
        self.Pre_select_GPIB_Addres.set(global_GPIB_COM[0])        
        # Frame Connection GPIB
        self.ConnectionGPIB_Contains = LabelFrame(self.Linha1, text="Connection GPIB", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.ConnectionGPIB_Contains.pack(side=LEFT, padx=10, pady=10)

        self.GPIB_Label = Label(self.ConnectionGPIB_Contains, text="GPIB Address ", font=("Calibri", "10"))
        self.GPIB_Label.grid(row=0,column=0,sticky="w", padx=(0,10))
        
        self.Option_GPIB_Addres = OptionMenu(self.ConnectionGPIB_Contains, self.Pre_select_GPIB_Addres,*global_GPIB_COM)
        self.Option_GPIB_Addres.grid(row=0, column=1, sticky="e", padx=(0,10))
        
        self.Button_Connection = Button(self.ConnectionGPIB_Contains, text="Connect", font=("Calibri", "10"),command=self.ConnectionGPIB_Command)
        self.Button_Connection.grid(row=0, column=2, sticky="w", padx=(0,10))
        
        self.ConnectionGPIB_Contains.grid_columnconfigure(0,weight=1)

    def Escale_Frame(self):
        self.Pre_Select_Corrente = StringVar(self)
        self.Pre_Select_Corrente.set(global_Escala_Corrente[3])        
        self.Pre_Select_Tensao = StringVar(self)
        self.Pre_Select_Tensao.set(global_Escala_Tensao[3])        

        self.Escala_Contains = LabelFrame(self.Linha1, text="Escala", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Escala_Contains.pack(side=TOP,padx=10,pady=10)
        
        self.Corrente_Label = Label(self.Escala_Contains, text="Corrente ", font=("Calibri","10"))
        self.Corrente_Label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.Corrente_Select = OptionMenu(self.Escala_Contains,self.Pre_Select_Corrente,*global_Escala_Corrente)
        self.Corrente_Select.grid(row=0, column=1, sticky="e", padx=(0, 10))
        self.Corrente_Unit_label = Label(self.Escala_Contains, text="[Amper]", font=("Calibri","10"))
        self.Corrente_Unit_label.grid(row=0, column= 2, sticky="w", padx=(0, 10))
        
        self.Voltage_Label = Label(self.Escala_Contains, text="Tensao ", font=("Calibri","10"))
        self.Voltage_Label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.Voltage_Select = OptionMenu(self.Escala_Contains,self.Pre_Select_Tensao,*global_Escala_Tensao)
        self.Voltage_Select.grid(row=1, column=1, sticky="e", padx=(0, 10))
        self.Voltage_Unit_label = Label(self.Escala_Contains, text="[Volts]", font=("Calibri","10"))
        self.Voltage_Unit_label.grid(row=1, column= 2, sticky="w", padx=(0, 10))
        
        self.Escala_Contains.grid_columnconfigure(0, weight=1)
        self.Escala_Contains.grid_columnconfigure(1, weight=1)        
        
    def Set_Measurement_Frame(self):
        self.Set_Contains = LabelFrame(self.Linha2, text="Set Measurement", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Set_Contains.pack(side=LEFT,padx=10,pady=10)        
        
        self.Nval_Label = Label(self.Set_Contains, text="Numero de aquisicoes: ", font=("Calibri", "10"))
        self.Nval_Label.grid(row=0,column=0, sticky="w",padx=(0, 10))
        self.Nval_Entry = Entry(self.Set_Contains,width=5)
        self.Nval_Entry.grid(row=0, column=1, sticky="e",padx=(0,10))
        
        self.TimeMens_Label = Label(self.Set_Contains, text="Tempo entre medidas: ", font=("Calibri", "10"))
        self.TimeMens_Label.grid(row=1, column=0, sticky="w", padx=(0,10))
        self.TimeMens_Entry = Entry(self.Set_Contains, width=5)
        self.TimeMens_Entry.grid(row=1,column=1,sticky="e",padx=(0,10))
        self.TimeMens_Unit_label = Label(self.Set_Contains, text="[Seg]", font=("Calibri", "10"))
        self.TimeMens_Unit_label.grid(row=1, column=2,sticky="w",padx=(0,10))
        
        self.MaxTime_Label = Label(self.Set_Contains, text="Tempo maximo de duracao: ",font=("Calibri","10"))
        self.MaxTime_Label.grid(row=2, column=0, sticky="w", padx=(0,10))
        self.MaxTime_Entry = Entry(self.Set_Contains, width=5)
        self.MaxTime_Entry.grid(row=2, column=1, sticky="e", padx=(0,10))
        self.MaxTime_Unit_Label = Label(self.Set_Contains, text="[Horas]", font=("Calibri", "10"))
        self.MaxTime_Unit_Label.grid(row=2, column=2, sticky="w",padx=(0,10))
        
        self.Set_Contains.grid_columnconfigure(0, weight=1)
        self.Set_Contains.grid_columnconfigure(1, weight=1)          
        self.Set_Contains.grid_columnconfigure(2, weight=1)
        
    def Start_Frame(self):
        self.Start_Contains = LabelFrame(self.Linha2, text="Start", font=("Calibri", "10", "bold"), padx=25, pady=10)
        self.Start_Contains.pack(side=TOP,padx=10,pady=10)

        self.FileName_Label = Label(self.Start_Contains, text="Nome do Arquivo [csv]", font=("Calibri","10"))
        self.FileName_Label.grid(row=0, column=0, sticky="w", padx=(0,10))
       
        self.FileName_Entry = Entry(self.Start_Contains, width=24)
        self.FileName_Entry.grid(row=1, column=0, sticky="w", padx=(0,10))
        
        self.FileName_Button = Button(self.Start_Contains,text="START",width=20,command=self.Start_Application)
        self.FileName_Button.grid(row=2,column=0, sticky="w", padx=(0,10))
        
    def Log_Frame(self):
        self.Log_Contains = LabelFrame(self.Linha3, text="Log das Medidas", font=("Calibri","10"), padx=35,pady=20)
        self.Log_Contains.pack(side=TOP)

        self.log_text = scrolledtext.ScrolledText(self.Log_Contains, width=60, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.Cancelar_button = Button(self.Log_Contains, text="Cancelar",width = 25)
        self.Cancelar_button.grid(row=1, column=0,sticky="w", padx=(0, 10))
       
    # Funcoes de operacao:
        
    def ConnectionGPIB_Command(self):
        global GPIBAdd
        GPIBAdd = self.Pre_select_GPIB_Addres.get()
        try:
            rm = pyvisa.ResourceManager()
            self.instrument = rm.open_resource(f'GPIB0::{GPIBAdd}::INSTR')
            self.instrument.timeout = 5000
            idn = self.instrument.query('*IDN?')
            
           
            info = f"Name: {idn}\nRsInstrument Conected!"
            messagebox.showinfo("Instrument info", info)
        except Exception as e:
            messagebox.showerror("Error", f"Connections Fail!\n{e}")
            return

    def write_sample(self,command):
        self.instrument.write(command)
        time.sleep(0.1)

    def read_sample(self,command):
        responde = self.instrument.query(command)
        time.sleep(0.1)
        return response
    
    def string_para_inteiro(self,s):
        try:
            return int(s)
        except ValueError:
            print(f"Erro: '{s}' nao e uma string numerica valida.")
            return None

    def Start_Application(self):
        global CSVname
        CSVname = self.FileName_Entry.get()
        global RequestValue
        RequestValue = int(self.Nval_Entry.get())
        global RequestValueTime
        RequestValueTime = int(self.MaxTime_Entry.get())
        try:
            self.configure_wattmeter()
            self.write_sample("INTEGRATE:START")
            with open(f'{CSVname}.csv', mode="w",newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Index", "Date", "Time", "Tensao (V)", "Corrente (A)", "Potencia (W)", "Potencia (VA)", "Potencia (VAR)", "Fator de Potencia", "Angulo (Grau)", "Frequencia (Hz)", "Energia (Wh)", "Energia (Wh+)"])

                prox_aq = datetime.now() + timedelta(hours=RequestValueTime)
                

                for x in range(RequestValue):
                    now = datetime.now()
                    if now <= prox_aq:
                        date_str = now.strftime("%Y-%m-%d")
                        time_str = now.strftime("%H:%M:%S")
                        
                        # Enviar comando e ler resposta
                        response = self.read_sample("MEASURE:VAL?")
                        values = response.split(',')
                        
                        # Converter valores para decimal
                        values_decimal = self.convert_to_decimal(values)
                        
                        # Escrever valores no CSV
                        row = [x, date_str, time_str] + values_decimal[:9] + values_decimal[9:12]
                        writer.writerow(row)
                       
                        self.log_text.insert(tk.END, row)
                        
                        # Atualizar próximo horário de aquisicao
                        #prox_aq = now + timedelta(seconds=1)
                        time.sleep(1) # Espera 1 Segundo para pegar a proxima medida
        except Exception as e:
            messagebox.showerror("Error", f"Connections Fail!\n{e}")
            return
        
    def convert_to_decimal(self,values):
        return [f"{float(value):.5f}" for value in values]

    def configure_wattmeter(self):
        commands = [
            "*RST"
            "CONFIGURE:MODE RMS",
            "SAMPLE:RATE 0.1",
            "CONFIGURE:SYNC CURRENT",
            "CONFIGURE:FILTER OFF",
            "CONFIGURE:LFILTER OFF",
            "CONFIGURE:AVERAGING:STATE OFF",
            "CONFIGURE:AVERAGING:TYPE LINEAR,8",
            "CONFIGURE:SCALING:STATE OFF",
            "CONFIGURE:SCALING:PT:ELEMENT1 1000",
            "CONFIGURE:SCALING:CT:ELEMENT1 1000",
            "CONFIGURE:SCALING:SFACTOR:ELEMENT1 1000",
            "CONFIGURE:VOLTAGE:RANGE 150",
            "CONFIGURE:CURRENT:RANGE 5",
            "MEAS:NORM:ITEM:V ON",
            "MEAS:NORM:ITEM:A ON",
            "MEAS:NORM:ITEM:W ON",
            "MEAS:NORM:ITEM:VA ON",
            "MEAS:NORM:ITEM:VAR ON",
            "MEAS:NORM:ITEM:PF ON",
            "MEAS:NORM:ITEM:DEGR ON",
            "MEAS:NORM:ITEM:VHZ ON",
            "MEAS:NORM:ITEM:AHZ ON",
            "MEAS:NORM:ITEM:WH ON",
            "MEAS:NORM:ITEM:WHP ON",
            "MEAS:NORM:ITEM:WHM ON",
            "MEAS:NORM:ITEM:AH ON",
            "MEAS:NORM:ITEM:AHP ON",
            "MEAS:NORM:ITEM:AHM ON",
            "MEAS:NORM:ITEM:VPK ON",
            "MEAS:NORM:ITEM:APK ON",
            "INTEGRATE:MODE NORMAL",
            "INTEGRATE:RESET"
        ]

        for command in commands:
            self.write_sample(command)
            time.sleep(0.1)

def main():
    root = tk.Tk()
    app = MainProgram(root)
    root.mainloop()

if __name__ == "__main__":
    main()
