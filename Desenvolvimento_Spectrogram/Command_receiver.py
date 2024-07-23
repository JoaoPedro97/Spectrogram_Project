import time
import pandas as pd
from datetime import datetime
from RsInstrument import RsInstrument

# Configuracao do endereco IP do analisador
global_ip = "192.168.0.111"  # Atualize com o IP correto do seu analisador
instr = RsInstrument(f"TCPIP::{global_ip}::INSTR", True, False)

# Funcao para medir a frequencia
def measure_frequency():
    # Comando SCPI para ler a frequencia
    instr.write_str(f"SENS:FREQ:CW:AFC ONCE")
    time.sleep(3)
    frequency = instr.query_str(f"FREQ:CENT?")
    return float(frequency)

# Configuracao inicial
tuned_frequency = "467500000.0"
data = []
var = 0
# Loop de medicao
try:
    while True:
        rf_frequency = measure_frequency()
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data.append([tuned_frequency, rf_frequency, current_time,var])
        
        var +=1
        
        print(f"Medicao {var}: Tuned Frequency: {tuned_frequency}, RF Frequency: {rf_frequency}, Time: {current_time}")

        # Salvar os dados em um CSV
        df = pd.DataFrame(data, columns=["Tuned Frequency", "RF Frequency", "Time", "Num"])
        df.to_csv("frequency_stability_TESTE-467-5.csv", index=False)
        
        
        
        # Esperar 1 segundo antes de medir novamente
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Medicao interrompida pelo usuario.")

finally:
    instr.close()
