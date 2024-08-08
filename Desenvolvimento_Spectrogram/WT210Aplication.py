# -*- coding: utf-8 -*-
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
from tkinter import filedialog

global_GPIB_COM = ["0","1","2","3","4","5","6","7","8","9"]
global_Escala_Corrente = ["0.5","1","2","5","10","20","AUTO"]
global_Escala_Tensao = ["15","30","60","150","300","600","AUTO"]

class MainProgram(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry("850x650")
        self.master.title("WT210 Application Measurement")
        self.cancel_measurement = False

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
        self.TimeMens_Unit_label = Label(self.Set_Contains, text="[mSeg]", font=("Calibri", "10"))
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
        self.Start_Contains.pack(side=TOP, padx=10, pady=10)
    
        self.FileName_Label = Label(self.Start_Contains, text="Caminho da pasta ou Nome:", font=("Calibri", "10"))
        self.FileName_Label.grid(row=0, column=0, sticky="w", padx=(0, 10))
    
        self.FileName_Entry = Entry(self.Start_Contains, width=45)
        self.FileName_Entry.grid(row=1, column=0, sticky="w", padx=(0, 10))
    
        self.FileName_Button = Button(self.Start_Contains, text="START", width=20, command=self.Start_Application)
        self.FileName_Button.grid(row=2, column=0, sticky="w", padx=(0, 10))

        self.ChooseLocation_Button = Button(self.Start_Contains, text="Escolher Local", width=20, command=self.choose_save_location)
        self.ChooseLocation_Button.grid(row=2, column=0, sticky="w", padx=(165, 0))
    
    def choose_save_location(self):
        # Abrir dialogo para o usuario escolher o local e nome do arquivo CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.FileName_Entry.delete(0, tk.END)
            self.FileName_Entry.insert(0, file_path)
        
    def Log_Frame(self):
        self.Log_Contains = LabelFrame(self.Linha3, text="Log das Medidas", font=("Calibri","10"), padx=35,pady=20)
        self.Log_Contains.pack(side=TOP)

        self.log_text = scrolledtext.ScrolledText(self.Log_Contains, width=100, height=15,font=("Arial","10"), wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.Cancelar_button = Button(self.Log_Contains, text="Cancelar", width=25, command=self.cancel_measurement)
        
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
        response = self.instrument.query(command)
        time.sleep(0.1)
        return response
            
    def Start_Application(self):
        try:
            global CSVname
            CSVname = self.FileName_Entry.get()
            global RequestValue
            RequestValue = int(self.Nval_Entry.get())
            global RequestValueTime
            RequestValueTime = int(self.MaxTime_Entry.get())   
            
            self.cancel_measurement = False
    
            self.configure_wattmeter()
            self.write_sample("INTEGRATE:START")
    
            self.file = open(f'{CSVname}.csv', mode="w", newline='')
            self.writer = csv.writer(self.file, delimiter=';') 
            self.writer.writerow(["Index", "Date", "Time", "Tensao (V)", "Corrente (A)", "Potencia (W)", "Potencia (VA)", "Potencia (VAR)", "Fator de Potencia", "Angulo (Grau)", "Frequencia (Hz)", "Energia (Wh)", "Energia (Wh+)"])
    
            self.prox_aq = datetime.now() + timedelta(hours=RequestValueTime)
            self.current_index = 0
            self.max_index = RequestValue
    
            self.schedule_next_measurement()
        except pyvisa.VisaIOError:
            messagebox.showerror("Erro de Conexao", "Nao foi possivel conectar ao dispositivo GPIB.")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, verifique os valores de entrada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            self.running = False

    def choose_save_location(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.FileName_Entry.delete(0, tk.END)
            self.FileName_Entry.insert(0, file_path)

    def schedule_next_measurement(self):
        global TimeSet
        TimeSet = int(self.TimeMens_Entry.get())
        now = datetime.now()
        if self.current_index < self.max_index and now <= self.prox_aq:
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")

            # Aguardar um breve periodo para garantir que o equipamento esteja pronto para a primeira medicao
            if self.current_index == 0:
                time.sleep(2)  # Ajuste esse valor conforme necessario

            response = self.read_sample("MEASURE:VAL?")
            values = response.split(',')
            
            if self.cancel_measurement:
                self.file.close()
                self.log_text.insert(tk.END, "Medicoes canceladas.\n")
                return

            # Verificar se a resposta tem o numero correto de valores esperados
            if len(values) == 11:
                values_decimal = self.convert_to_decimal(values)

                row = [self.current_index, date_str, time_str] + values_decimal[:9] + values_decimal[9:12]
                self.writer.writerow(row)

                self.log_text.insert(tk.END, f"{row}\n")
                self.log_text.see(tk.END)  # Scroll to the end of the log_text

            else:
                self.log_text.insert(tk.END, f"Erro na leitura dos valores: {response}\n")
                self.log_text.see(tk.END)

            self.current_index += 1
            self.master.after(TimeSet, self.schedule_next_measurement)  # Schedule next measurement after TimeSet
        else:
            self.file.close()
            self.log_text.insert(tk.END, "Medicoes concluidas.\n")

    def convert_to_decimal(self,values):
        return [f"{float(value):.2f}".replace('.', ',') for value in values]
    
    def cancel_measurement(self):
        self.cancel_measurement = True
        self.master.after_cancel(self.schedule_next_measurement)

    def configure_wattmeter(self):
        Corrent = self.Pre_Select_Corrente.get()
        Tensao = self.Pre_Select_Tensao.get()
        commands = [
            "*RST",
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
            f"CONFIGURE:VOLTAGE:RANGE {Tensao}",
            f"CONFIGURE:CURRENT:RANGE {Corrent}",
            "MEAS:NORM:ITEM:V ON",
            "MEAS:NORM:ITEM:A ON",
            "MEAS:NORM:ITEM:W ON",
            "MEAS:NORM:ITEM:VA ON",
            "MEAS:NORM:ITEM:VAR ON",
            "MEAS:NORM:ITEM:PF ON",
            "MEAS:NORM:ITEM:DEGR ON",
            "MEAS:NORM:ITEM:VHZ ON",
            "MEAS:NORM:ITEM:AHZ OFF",
            "MEAS:NORM:ITEM:WH ON",
            "MEAS:NORM:ITEM:WHP ON",
            "MEAS:NORM:ITEM:WHM ON",
            "MEAS:NORM:ITEM:AH OFF",
            "MEAS:NORM:ITEM:AHP OFF",
            "MEAS:NORM:ITEM:AHM OFF",
            "MEAS:NORM:ITEM:VPK OFF",
            "MEAS:NORM:ITEM:APK OFF",
            "INTEGRATE:MODE NORMAL",
            "INTEGRATE:RESET"
        ]

        for command in commands:
            self.write_sample(command)
            time.sleep(0.5)

def main():
    root = tk.Tk()
    app = MainProgram(root)
    root.mainloop()

if __name__ == "__main__":
    main()
