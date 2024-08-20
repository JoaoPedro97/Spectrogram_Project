import serial
import csv
import time

# Configuracao da porta serial (ajuste conforme necessario)
serial_port = 'COM5'  # Substitua pela porta correta (no Windows) ou /dev/ttyUSB0 (Linux)
baud_rate = 115200
timeout = 1

# Nome do arquivo CSV
csv_filename = "medicoes.csv"

# Abrir a porta serial
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
time.sleep(2)  # Esperar a inicializacao da porta serial

# Abrir o arquivo CSV para gravacao
with open(csv_filename, mode='w', newline='') as file:
    csv_writer = csv.writer(file, delimiter=';')  # Usando o delimitador `;`
    
    # Cabecalho
    csv_writer.writerow(["N Medida", "Data", "Hora", "Tensao (V)", "Corrente (A)", "Potencia (W)", "Porcentagem da Bateria (%)", "Wh Consumido (Wh)"])

    # Capturar e salvar os dados
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            # Obter a data e hora atuais
            current_time = time.localtime()
            date_str = time.strftime("%Y-%m-%d", current_time)
            time_str = time.strftime("%H:%M:%S", current_time)

            # Imprimir no terminal e salvar no CSV
            print(line)
            csv_writer.writerow([line.split(";")[0], date_str, time_str] + line.split(";")[1:])
            
        # Condicao de parada (opcional, ajuste conforme necessario)
        if "STOP" in line:
            break

# Fechar a porta serial
ser.close()
