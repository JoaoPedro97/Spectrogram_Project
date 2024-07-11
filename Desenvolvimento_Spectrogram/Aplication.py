from tkinter import *
from tkinter import messagebox
from RsInstrument.RsInstrument import RsInstrument

class MainProgram():
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x650")
        self.master.title("Spectrogram Alfa")

        self.create_widgets_TestConnection()
        self.create_Ensaios_Bluetooth()

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
            self.lb.delete(0, END)
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
        self.command_template([
            "*RST",
            "BAND 100kHz",
            "BAND:VID 300kHz",
            "DISP:WIND:TRAC:Y:RLEV 10dBm",
            "DISP:WIND:TRAC:MODE MAXH",
            f"FREQ:CENT {self.LarguraEntry.get()} MHz",
            "FREQ:SPAN 3 MHz"
        ])

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
            "SWE:TIME 20 ms",
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
            "SWE:TIME 20 ms",
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
            "SWE:TIME 20 ms",
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
            "SWE:TIME 20 ms",
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

    def Inicio_Largura20dB(self):
        self.execute_command(self.Command_Largura20dB)

    def Inicio_Potencia(self):
        self.execute_command(self.Command_Potencia)

    def Inicio_NumeroFreq01(self):
        self.execute_command(self.Command_NumeroFreq01)

    def Inicio_NumeroFreq02(self):
        self.execute_command(self.Command_NumeroFreq02)

    def Inicio_Num_Util(self):
        self.execute_command(self.Command_Num_Util)

    def Inicio_Temp_Dur(self):
        self.execute_command(self.Command_Temp_Dur)

    def Inicio_Espur01(self):
        self.execute_command(self.Command_Espur01)

    def Inicio_Espur02(self):
        self.execute_command(self.Command_Espur02)

    def Inicio_Espur03(self):
        self.execute_command(self.Command_Espur03)

    def Inicio_Espur04(self):
        self.execute_command(self.Command_Espur04)

def main():
    root = Tk()
    app = MainProgram(root)
    root.mainloop()

if __name__ == "__main__":
    main()
