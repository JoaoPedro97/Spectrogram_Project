import tkinter as tk
from tkinter import messagebox
from RsInstrument.RsInstrument import RsInstrument

class ConnectionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x200")
        self.title("Conexao com IP")
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self, text="IP:")
        self.ip_label.pack(pady=10)

        self.ip_entry = tk.Entry(self, width=20)
        self.ip_entry.pack(pady=10)

        self.connect_button = tk.Button(self, text="Connect", command=self.authenticate)
        self.connect_button.pack(pady=10)

    def authenticate(self):
        ip_val = self.ip_entry.get()
        try:
            self.resource_string_1 = f'TCPIP::{ip_val}::INSTR'
            self.instr = RsInstrument(self.resource_string_1, True, False)
            idn = self.instr.query_str('*IDN?')
            driver = self.instr.driver_version
            visa_manufacturer = self.instr.visa_manufacturer
            instrument_full_name = self.instr.full_instrument_model_name

            info = f"Name: {idn}\nRsInstrument Driver Version: {driver}\nVisa Manufacturer: {visa_manufacturer}\nInstrument Full Name: {instrument_full_name}"
            messagebox.showinfo("Instrument informations", info)
            self.master.lb.insert(tk.END, 'Name: ' + idn)
            self.master.lb.insert(tk.END, 'RsInstrument Driver Version: ' + driver)
            self.master.lb.insert(tk.END, 'Visa Manufacturer: ' + visa_manufacturer)
            self.master.lb.insert(tk.END, 'Instrument full name: ' + instrument_full_name)
            self.master.lb.insert(tk.END, 'Instrument Installed Options: ' + ",".join(self.instr.instrument_options))
            self.master.lb.insert(tk.END, "Connection Success")
            self.master.lb.itemconfig(tk.END, {'fg': 'green'})
        except Exception as e:
            messagebox.showerror("Error", f"Connections Fail!\n{e}")
            self.master.lb.delete(0, tk.END)

class TestConnectionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x300")
        self.title("Informacoes de Conexao")
        self.create_widgets()

    def create_widgets(self):
        self.container_2 = tk.LabelFrame(self, text="Dados do equipamento", pady=5)
        self.container_2.pack(side=tk.TOP, padx=10, pady=10)

        self.lb = tk.Listbox(self.container_2, width=45, height=10)
        self.lb.pack(side=tk.TOP, expand=True)

class BluetoothWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("500x400")
        self.title("Ensaios de Bluetooth - Presets")
        self.create_widgets()

    def create_widgets(self):
        self.ensaios_bluetooth = tk.LabelFrame(self, text="Ensaios de Bluetooth - Presets", padx=10, pady=10)
        self.ensaios_bluetooth.pack(side=tk.TOP, fill="both", expand=True)

        ensaios = [
            ("Espacamento", master.Command_Espacamento, "Freq", "EspacamentoEntry", "MHz"),
            ("Largura de faixa a 20 dB", master.Command_Largura20dB, "Freq", "LarguraEntry", "MHz"),
            ("Potencia de pico maxima de saida", master.Command_Potencia, "Freq", "PotenciaEntry", "MHz"),
            ("Numero de frequencias de salto", master.Command_NumeroFreq01, " 2.400 GHz a 2.4405 GHz ", None, "01"),
            ("Numero de frequencias de salto", master.Command_NumeroFreq02, " 2.4405 GHz a 2.4835 GHz ", None, "02"),
            ("Numero de utilizacoes", master.Command_Num_Util, " 2.442 ", None, "GHz"),
            ("Tempo de duracao de um Slot", master.Command_Temp_Dur, " 2.442 ", None, "GHz"),
            ("Espurios 30 MHz a 2.402 GHz", master.Command_Espur01, None, None, None),
            ("Espurios 2.302 GHz a 2.402 GHz", master.Command_Espur02, None, None, None),
            ("Espurios 2.480 GHz a 2.580 GHz", master.Command_Espur03, None, None, None),
            ("Espurios 2.480 GHz a 18 GHz", master.Command_Espur04, None, None, None)
        ]

        for ensaio in ensaios:
            self.add_ensaio(*ensaio)

    def add_ensaio(self, text, command, label_text, entry_attr, unit_text):
        frame = tk.Frame(self.ensaios_bluetooth)
        frame.pack(anchor="w", pady=5)

        button = tk.Button(frame, text=text, command=command, width=28)
        button.pack(side=tk.LEFT)

        if label_text:
            label = tk.Label(frame, text=label_text)
            label.pack(side=tk.LEFT)

        if entry_attr:
            entry = tk.Entry(frame)
            setattr(self.master, entry_attr, entry)
            entry.pack(side=tk.LEFT)

        if unit_text:
            unit = tk.Label(frame, text=unit_text)
            unit.pack(side=tk.LEFT)

class MainProgram():
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x200")
        self.master.title("Spectrogram Alfa")

        self.connection_button = tk.Button(master, text="Conexao com IP", command=self.open_connection_window)
        self.connection_button.pack(pady=10)

        self.test_connection_button = tk.Button(master, text="Informacoes de Conexao", command=self.open_test_connection_window)
        self.test_connection_button.pack(pady=10)

        self.bluetooth_button = tk.Button(master, text="Ensaios Bluetooth", command=self.open_bluetooth_window)
        self.bluetooth_button.pack(pady=10)

    def open_connection_window(self):
        ConnectionWindow(self.master)

    def open_test_connection_window(self):
        TestConnectionWindow(self.master)

    def open_bluetooth_window(self):
        BluetoothWindow(self.master)

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

def main():
    root = tk.Tk()
    app = MainProgram(root)
    root.mainloop()

if __name__ == "__main__":
    main()
