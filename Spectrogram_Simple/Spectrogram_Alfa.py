from tkinter import *
from tkinter import messagebox
from RsInstrument.RsInstrument import RsInstrument

class MainProgram():
    def __init__(self, master): #Abre a tela principal
        self.master = master
        self.master.geometry("500x650")
        self.master.title("Spectrogram Alfa")

        self.create_widgets_TestConnection()
        self.create_Ensaios_Bluetooth()

    def create_widgets_TestConnection(self):
        self.fonte = ("Verdana","8")

        self.Container_1 = LabelFrame(text="Instrument Connection")
        self.Container_1["padx"] = 10
        self.Container_1["pady"] = 10
        self.Container_1.pack(side = TOP)

        self.FirthPackIP = Frame(self.Container_1)
        self.FirthPackIP.pack(side = TOP)

        self.LABIP = Label(self.FirthPackIP, text = "IP")
        self.LABIP["font"] = ("Calibri","12","bold")
        self.LABIP.pack(side=LEFT)

        self.EntradaIP = Entry(self.FirthPackIP)
        self.EntradaIP["font"] = ("Arial","10")
        self.EntradaIP["width"] = 15
        self.EntradaIP.pack(side=LEFT)

        self.ConnectingButton = Button(self.FirthPackIP, text="Connect", command=self.authenticate)
        self.ConnectingButton["font"] = ("Calibri","10")
        self.ConnectingButton["width"] = 15
        self.ConnectingButton.pack(side=RIGHT)

        self.Container_2 = LabelFrame(self.Container_1,text = "Dados do equipamento")
        self.Container_2["pady"] = 5
        self.Container_2.pack(side=TOP)

        self.lb = Listbox(self.Container_2, width=45, height=6)  # Ajustando a altura do Listbox para 6 itens
        self.lb.pack(side=TOP, expand=True)
        

        self.Container_3 = Frame(self.Container_1)
        self.Container_3["padx"] = 10
        self.Container_3["pady"] = 10
        self.Container_3.pack()

    def authenticate(self):
        ip_val = self.EntradaIP.get()

        try:
            self.resource_string_1 = f'TCPIP::{ip_val}::INSTR'
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
            self.lb.delete(0, END)  # Limpa o Listbox antes de inserir as informacoes
            self.info_instrument()

    def info_instrument(self):
        ip_val = self.EntradaIP.get()
        resource_string_1 = f'TCPIP::{ip_val}::INSTR'
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
        self.EnsaiosBluetooth = LabelFrame(text="Ensaios de Bluetooth - Presets")
        self.EnsaiosBluetooth.pack(side=TOP, padx=10, pady=10)

        # Espacamento
        self.EnsaiosBluetooth_Espacamento = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Espacamento.pack(anchor="w", pady=5)

        self.Preset_Espacamento = Button(self.EnsaiosBluetooth_Espacamento, text="Espacamento")
        self.Preset_Espacamento["command"] = self.Inicio_Espacamento
        self.Preset_Espacamento["width"] = 28
        self.Preset_Espacamento.pack(side=LEFT)

        self.EspacamentoLabelFreq = Label(self.EnsaiosBluetooth_Espacamento, text="Freq")
        self.EspacamentoLabelFreq.pack(side=LEFT)

        self.EspacamentoEntry = Entry(self.EnsaiosBluetooth_Espacamento)
        self.EspacamentoEntry.pack(side=LEFT)

        self.EspacamentoUnit = Label(self.EnsaiosBluetooth_Espacamento, text="MHz")
        self.EspacamentoUnit.pack(side=LEFT)

        # Largura de faixa a 20 dB
        self.EnsaiosBluetooth_Largura = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Largura.pack(anchor="w", pady=5)

        self.Preset_Largura_20dB = Button(self.EnsaiosBluetooth_Largura, text="Largura de faixa a 20 dB")
        self.Preset_Largura_20dB["command"] = self.Inicio_Largura20dB
        self.Preset_Largura_20dB["width"] = 28
        self.Preset_Largura_20dB.pack(side=LEFT)

        self.LarguraLabelFreq = Label(self.EnsaiosBluetooth_Largura, text="Freq")
        self.LarguraLabelFreq.pack(side=LEFT)

        self.LarguraEntry = Entry(self.EnsaiosBluetooth_Largura)
        self.LarguraEntry.pack(side=LEFT)

        self.LarguraUnit = Label(self.EnsaiosBluetooth_Largura, text="MHz")
        self.LarguraUnit.pack(side=LEFT)

        # Potencia de pico maximo
        self.EnsaiosBluetooth_Potencia = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Potencia.pack(anchor="w", pady=5)

        self.Preset_Potencia = Button(self.EnsaiosBluetooth_Potencia, text="Potencia de pico maxima de saida")
        self.Preset_Potencia["command"] = self.Inicio_Potencia
        self.Preset_Potencia["width"] = 28
        self.Preset_Potencia.pack(side=LEFT)

        self.PotenciaLabelFreq = Label(self.EnsaiosBluetooth_Potencia, text="Freq")
        self.PotenciaLabelFreq.pack(side=LEFT)

        self.PotenciaEntry = Entry(self.EnsaiosBluetooth_Potencia)
        self.PotenciaEntry.pack(side=LEFT)

        self.PotenciaUnit = Label(self.EnsaiosBluetooth_Potencia, text="MHz")
        self.PotenciaUnit.pack(side=LEFT)

        #Numero de frequencias de salto 01
        self.EnsaiosBluetooth_NumFreqSalt01 = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_NumFreqSalt01.pack(anchor="w", pady=5)

        self.Preset_NumFreqSalt01 = Button(self.EnsaiosBluetooth_NumFreqSalt01, text="Numero de frequencias de salto")
        self.Preset_NumFreqSalt01["command"] = self.Inicio_NumeroFreq01
        self.Preset_NumFreqSalt01["width"] = 28
        self.Preset_NumFreqSalt01.pack(side=LEFT)

        self.LarguraLabelFreq = Label(self.EnsaiosBluetooth_NumFreqSalt01, text=" 2.400 GHz a 2.4405 GHz ")
        self.LarguraLabelFreq.pack(side=LEFT)

        self.NumFreqSalt01Unit = Label(self.EnsaiosBluetooth_NumFreqSalt01, text="01")
        self.NumFreqSalt01Unit.pack(side=LEFT)

        #Numero de frequencias de salto 02
        self.EnsaiosBluetooth_NumFreqSalt02 = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_NumFreqSalt02.pack(anchor="w", pady=5)

        self.Preset_NumFreqSalt02 = Button(self.EnsaiosBluetooth_NumFreqSalt02, text="Numero de frequencias de salto")
        self.Preset_NumFreqSalt02["command"] = self.Inicio_NumeroFreq02
        self.Preset_NumFreqSalt02["width"] = 28
        self.Preset_NumFreqSalt02.pack(side=LEFT)

        self.LarguraLabelFreq = Label(self.EnsaiosBluetooth_NumFreqSalt02, text=" 2.4405 GHz a 2.4835 GHz ")
        self.LarguraLabelFreq.pack(side=LEFT)

        self.NumFreqSalt02Unit = Label(self.EnsaiosBluetooth_NumFreqSalt02, text="02")
        self.NumFreqSalt02Unit.pack(side=LEFT)

        #Numero de utilizacoes 
        self.EnsaiosBluetooth_Num_Utiliz = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Num_Utiliz.pack(anchor="w", pady=5)

        self.Preset_Num_Utiliz = Button(self.EnsaiosBluetooth_Num_Utiliz, text="Numero de utilizacoes")
        self.Preset_Num_Utiliz["command"] = self.Inicio_Num_Util
        self.Preset_Num_Utiliz["width"] = 28
        self.Preset_Num_Utiliz.pack(side=LEFT)

        self.Num_UtilizLabelFreq = Label(self.EnsaiosBluetooth_Num_Utiliz, text=" 2.442 ")
        self.Num_UtilizLabelFreq.pack(side=LEFT)
        
        self.Num_UtilizUnit = Label(self.EnsaiosBluetooth_Num_Utiliz, text="GHz")
        self.Num_UtilizUnit.pack(side=LEFT)
        
        #Tempo de duracao de um slot
        self.EnsaiosBluetooth_Tempo_Slot = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Tempo_Slot.pack(anchor="w", pady=5)

        self.Preset_Tempo_Slot = Button(self.EnsaiosBluetooth_Tempo_Slot, text="Tempo de duracao de um Slot")
        self.Preset_Tempo_Slot["command"] = self.Inicio_Temp_Dur
        self.Preset_Tempo_Slot["width"] = 28
        self.Preset_Tempo_Slot.pack(side=LEFT)

        self.Tempo_SlotLabelFreq = Label(self.EnsaiosBluetooth_Tempo_Slot, text=" 2.442 ")
        self.Tempo_SlotLabelFreq.pack(side=LEFT)
        
        self.Tempo_SlotUnit = Label(self.EnsaiosBluetooth_Tempo_Slot, text="GHz")
        self.Tempo_SlotUnit.pack(side=LEFT)

        #Espurios
        self.EnsaiosBluetooth_Espurios_01 = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Espurios_01.pack(anchor="w", pady=5)

        self.Preset_Espurios01 = Button(self.EnsaiosBluetooth_Espurios_01, text="Espurios 30 MHz a 2.402 GHz")
        self.Preset_Espurios01["command"] = self.Inicio_Espur01
        self.Preset_Espurios01["width"] = 28
        self.Preset_Espurios01.pack(side=LEFT)

        self.EnsaiosBluetooth_Espurios_02 = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Espurios_02.pack(anchor="w", pady=5)

        self.Preset_Espurios02 = Button(self.EnsaiosBluetooth_Espurios_02, text="Espurios 2.302 GHz a 2.402 GHz")
        self.Preset_Espurios02["command"] = self.Inicio_Espur02
        self.Preset_Espurios02["width"] = 28
        self.Preset_Espurios02.pack(side=LEFT)

        self.EnsaiosBluetooth_Espurios_03 = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Espurios_03.pack(anchor="w", pady=5)

        self.Preset_Espurios03 = Button(self.EnsaiosBluetooth_Espurios_03, text="Espurios 2.480 GHz a 2.580 GHz")
        self.Preset_Espurios03["command"] = self.Inicio_Espur03
        self.Preset_Espurios03["width"] = 28
        self.Preset_Espurios03.pack(side=LEFT)

        self.EnsaiosBluetooth_Espurios_04 = Frame(self.EnsaiosBluetooth)
        self.EnsaiosBluetooth_Espurios_04.pack(anchor="w", pady=5)

        self.Preset_Espurios04 = Button(self.EnsaiosBluetooth_Espurios_04, text="Espurios 2.480 GHz a 18 GHz")
        self.Preset_Espurios04["command"] = self.Inicio_Espur04
        self.Preset_Espurios04["width"] = 28
        self.Preset_Espurios04.pack(side=LEFT)

    def Command_Espacamento(self):
        self.instr.write_str("*RST")
        #Declaracao das variavies
        Freq = self.EspacamentoEntry.get()
        RBW = "BAND 100kHz"
        VBW = "BAND:VID 300kHz"
        Ref = "DISP:WIND:TRAC:Y:RLEV 10dBm"
        Att = "INP:ATT 30 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqSet = f"FREQ:CENT {Freq} MHz"
        SPAN = "FREQ:SPAN 3 MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqSet)
        self.instr.write_str(SPAN)
        self.instr.go_to_local()

    def Command_Largura20dB(self):
        self.instr.write_str("*RST")
        #Declaracao das Variavies
        Freq = self.LarguraEntry.get()
        RBW = "BAND 100kHz"
        VBW = "BAND:VID 300kHz"
        Ref = "DISP:WIND:TRAC:Y:RLEV 10dBm"
        Att = "INP:ATT 30 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqSet = f"FREQ:CENT {Freq} MHz"
        SPAN = "FREQ:SPAN 3 MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqSet)
        self.instr.write_str(SPAN)
        self.instr.go_to_local()

    def Command_Potencia(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        Freq = self.PotenciaEntry.get()
        RBW = "BAND 1 MHz"
        VBW = "BAND:VID 3 MHz"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqSet = f"FREQ:CENT {Freq} MHz"
        SPAN = "FREQ:SPAN 3 MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqSet)
        self.instr.write_str(SPAN)
        self.instr.go_to_local()

    def Command_NumeroFreq01(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        FStar = "2400"
        FStop = "2440.5"
        RBW = "BAND 100 kHz"
        VBW = "BAND:VID 100 kHz"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqStart = f"FREQ:START {FStar} MHz"
        FreqStop = f"FREQ:STOP {FStop} MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqStart)
        self.instr.write_str(FreqStop)
        self.instr.go_to_local()

    def Command_NumeroFreq02(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        FStar = "2440.5"
        FStop = "2483.5"
        RBW = "BAND 100 kHz"
        VBW = "BAND:VID 100 kHz"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqStart = f"FREQ:START {FStar} MHz"
        FreqStop = f"FREQ:STOP {FStop} MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqStart)
        self.instr.write_str(FreqStop)
        self.instr.go_to_local()

    def Command_Num_Util(self):
        #self.instr.write_str("*RST")
        #Declaracao das Variaveis
        Freq = "2442"
        RBW = "BAND 300 kHz"
        VBW = "BAND:VID 300 kHz"
        SWT = "SWE:TIME 1 s"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqCent = f"FREQ:START {Freq} MHz"
        SPAN = "FREQ:SPAN 0"
        #Codigo de preset
        self.instr.write_str(SPAN)
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(SWT)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqCent)
        self.instr.write_str("INIT:CONT OFF")
        self.instr.write_str("INIT:IMM")

        self.instr.go_to_local()

    def Command_Temp_Dur(self):
        #self.instr.write_str("*RST")
        #Declaracao das Variaveis
        Freq = "2442"
        RBW = "BAND 1 MHz"
        VBW = "BAND:VID 3 MHz"
        SWT = "SWE:TIME 0.02 "
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqCent = f"FREQ:START {Freq} MHz"
        SPAN = "FREQ:SPAN 0"
        #Codigo de preset
        self.instr.write_str(SPAN)
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(SWT)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqCent)
        self.instr.write_str("INIT:CONT OFF")
        self.instr.write_str("INIT:IMM")

        self.instr.go_to_local()

    def Command_Espur01(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        FStar = "30"
        FStop = "2402"
        RBW = "BAND 100 kHz"
        VBW = "BAND:VID 300 kHz"
        SWT = "SWE:TIME 20 ms"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqStart = f"FREQ:START {FStar} MHz"
        FreqStop = f"FREQ:STOP {FStop} MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqStart)
        self.instr.write_str(FreqStop)
        self.instr.go_to_local()

    def Command_Espur02(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        FStar = "2302"
        FStop = "2402"
        RBW = "BAND 100 kHz"
        VBW = "BAND:VID 300 kHz"
        SWT = "SWE:TIME 20 ms"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqStart = f"FREQ:START {FStar} MHz"
        FreqStop = f"FREQ:STOP {FStop} MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqStart)
        self.instr.write_str(FreqStop)
        self.instr.go_to_local()    

    def Command_Espur03(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        FStar = "2480"
        FStop = "2580"
        RBW = "BAND 100 kHz"
        VBW = "BAND:VID 300 kHz"
        SWT = "SWE:TIME 20 ms"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqStart = f"FREQ:START {FStar} MHz"
        FreqStop = f"FREQ:STOP {FStop} MHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqStart)
        self.instr.write_str(FreqStop)
        self.instr.go_to_local()        

    def Command_Espur04(self):
        self.instr.write_str("*RST")
        #Declaracao das Variaveis
        FStar = "2480"
        FStop = "18"
        RBW = "BAND 100 kHz"
        VBW = "BAND:VID 300 kHz"
        SWT = "SWE:TIME 20 ms"
        Ref = "DISP:WIND:TRAC:Y:RLEV 20dBm"
        Att = "INP:ATT 40 DB"
        MaxHold = "DISP:WIND:TRAC:MODE MAXH"
        FreqStart = f"FREQ:START {FStar} MHz"
        FreqStop = f"FREQ:STOP {FStop} GHz"
        #Codigo de preset
        self.instr.write_str(RBW)
        self.instr.write_str(VBW)
        self.instr.write_str(Ref)
        self.instr.write_str(MaxHold)
        self.instr.write_str(FreqStart)
        self.instr.write_str(FreqStop)
        self.instr.go_to_local()      

    def Inicio_Espacamento(self):
        try:
            self.Command_Espacamento()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Largura20dB(self):
        try:
            self.Command_Largura20dB()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Potencia(self):
        try:
            self.Command_Potencia()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_NumeroFreq01(self):
        try:
            self.Command_NumeroFreq01()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_NumeroFreq02(self):
        try:
            self.Command_NumeroFreq02()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Num_Util(self):
        try:
            self.Command_Num_Util()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Temp_Dur(self):
        try:
            self.Command_Temp_Dur()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Espur01(self):
        try:
            self.Command_Espur01()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Espur02(self):
        try:
            self.Command_Espur02()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Espur03(self):
        try:
            self.Command_Espur03()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")

    def Inicio_Espur04(self):
        try:
            self.Command_Espur04()
        except Exception as e:
            messagebox.showerror("Error", f"Command Fail!\n{e}")



def main():
    root = Tk()
    app = MainProgram(root)
    root.mainloop()

if __name__ == "__main__":
    main()
