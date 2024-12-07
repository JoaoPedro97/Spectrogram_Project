import time
import pandas as pd
from RsInstrument import RsInstrument

# Configuracao do endereco IP do analisador
global_ip = "192.168.0.111"  # Atualize com o IP correto do seu analisador
instr = RsInstrument(f"TCPIP::{global_ip}::INSTR", True, False)

# Funcao para configurar o analisador e medir a potencia
def measure_power(frequency):
    # Configura a frequencia central do analisador
    instr.write_str(f"FREQ:CENT {frequency} Hz")
    
    # Configura SPAN, RBW e VBW
    instr.write_str("FREQ:SPAN 30000 Hz")
    instr.write_str("BAND:RES 1000 Hz")
    instr.write_str("BAND:VID 3000 Hz")
    
    # Ativa o marcador e configura para encontrar o pico maximo
    instr.write_str("CALC:MARK1:MAX")
    time.sleep(2)  # Esperar um pouco para garantir a leitura correta
    
    # Consulta o valor da potencia
    power = instr.query_str("CALC:MARK1:Y?")
    power = float(power)
    # Limita a duas casas decimais
    power = round(power, 2)
    return power

# Solicita o numero de frequencias ao usuario
num_frequencies = int(input("Digite o numero de frequencias que deseja testar: "))
frequencies = []

# Solicita cada frequencia ao usuario
for i in range(num_frequencies):
    freq = float(input(f"Digite a frequencia {i+1} em MHz: "))
    frequencies.append(freq * 1e6)  # Converte MHz para Hz

# Lista para armazenar as medições de potencia
power_measurements = []

# Realiza as medições de potencia para cada frequencia
for frequency in frequencies:
    power = measure_power(frequency)
    power_measurements.append([frequency / 1e6, power])  # Converte de volta para MHz para salvar
    print(f"Frequencia: {frequency / 1e6} MHz, Potencia: {power} dBm")
    input("Configure o transmissor para a proxima frequencia e pressione Enter para continuar...")

# Cria o DataFrame com os resultados
df = pd.DataFrame(power_measurements, columns=["Frequencia [MHz]", "Potencia [dBm]"])

# Salva o resultado em um arquivo CSV
csv_filename = "Teste_Potencia_RF.csv"
df.to_csv(csv_filename, index=False, sep=';')

print(f"Resultados salvos em {csv_filename}")

# Fecha a conexao com o instrumento
instr.close()
