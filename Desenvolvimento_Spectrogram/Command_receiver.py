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
    # Limita o numero de caracteres da esquerda para direita em 9
    frequency = float(str(frequency)[:9])
    return int(frequency)

# Solicita a frequencia de operacao ao usuario
operation_frequency = float(input("Digite a frequencia de operacao em Hz: "))

# Lista para armazenar todas as medições
all_measurements = []

# Repetir o processo 3 vezes
for repetition in range(3):
    # Lista para armazenar as frequencias medidas em uma repetição
    frequencies = []

    # Realiza 4 medições
    for i in range(4):
        rf_frequency = measure_frequency()
        frequencies.append(rf_frequency)
        print(f"Repeticao {repetition+1}, Medicao {i+1}: RF Frequency: {rf_frequency} Hz")
        time.sleep(1)  # Esperar 1 segundo antes de medir novamente

    # Calcula a media das frequencias medidas
    average_frequency = sum(frequencies) / len(frequencies)

    # Calcula a variacao especificada
    specified_variation = (10 / 1000000) * operation_frequency

    # Calcula a variacao (diferenca entre maior e menor valor medido)
    measured_variation = max(frequencies) - min(frequencies)

    # Adiciona os resultados da repetição atual na lista geral
    all_measurements.append(frequencies + [average_frequency, specified_variation, measured_variation])

# Cria o DataFrame com os resultados
df = pd.DataFrame(all_measurements, columns=["Frequencia 1", "Frequencia 2", "Frequencia 3", "Frequencia 4", "Frequencia Media", "Variacao Especificada", "Variacao"])

# Salva o resultado em um arquivo CSV
csv_filename = f"Estabilidade_Frequencia-{int(operation_frequency)}.csv"
df.to_csv(csv_filename, index=False, sep=';')

print(f"Resultados salvos em {csv_filename}")

# Fecha a conexao com o instrumento
instr.close()
