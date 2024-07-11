import tkinter as tk
from tkinter import END, LEFT, RIGHT, TOP, Button, Entry, Frame, Label, LabelFrame, Listbox, messagebox
from RsInstrument.RsInstrument import RsInstrument
import os
from datetime import datetime

class MainWindows(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry("350x200")
        self.master.title("Spectrogram Alfa")

        self.create_widgets_TestConnection()  
        
    def create_widgets_TestConnection(self):
        self.fonte = ("Verdana", "8")

        self.Container_1 = LabelFrame(self, text="Instrument Connection", padx=10, pady=10)
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
            self.info_instrument(idn, driver, visa_manufacturer, instrument_full_name)
            self.save_log(idn, driver, visa_manufacturer, instrument_full_name)
            
    def info_instrument(self, idn, driver, visa_manufacturer, instrument_full_name):
        ip_val = self.EntradaIP.get()
        resource_string_1 = f'TCPIP::{ip_val}::INSTR'
        instr = RsInstrument(resource_string_1, True, False)

        self.lb.insert(END, 'Name: ' + idn)
        self.lb.insert(END, 'RsInstrument Driver Version: ' + driver)
        self.lb.insert(END, 'Visa Manufacturer: ' + visa_manufacturer)
        self.lb.insert(END, 'Instrument full name: ' + instrument_full_name)
        self.lb.insert(END, 'Instrument Installed Options: ' + ",".join(instr.instrument_options))
        self.lb.insert(END, "Connection Success")
        self.lb.itemconfig(END, {'fg': 'green'})

    def save_log(self, idn, driver, visa_manufacturer, instrument_full_name):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "instrument_log.csv")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"{idn};{driver};{visa_manufacturer};{instrument_full_name};{current_time}\n"
        
        with open(log_file, "a") as file:
            file.write(log_entry)
        messagebox.showinfo("Log Saved", "The log has been saved successfully.")

def main():
    root = tk.Tk()
    app = MainWindows(root)
    root.mainloop()

if __name__ == "__main__":
    main()
