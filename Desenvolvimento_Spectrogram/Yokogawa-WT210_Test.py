import pyvisa
import time
import csv
from datetime import datetime, timedelta

# Funcao para realizar a conexao e enviar comandos ao instrumento
def write_sample(command):
    instrument.write(command)
    time.sleep(0.1)

def read_sample(command):
    response = instrument.query(command)
    time.sleep(0.1)
    return response

# Função para converter notação científica para decimal
def convert_to_decimal(values):
    return [f"{float(value):.5f}" for value in values]


# Conexao com o instrumento
rm = pyvisa.ResourceManager()
instrument = rm.open_resource('GPIB0::1::INSTR')
instrument.timeout = 5000

# Funcao principal para realizar medicões e salvar em CSV
def main():
    # Iniciar integracao
    write_sample("INTEGRATE:START")
    #write_sample("*IDN?")
    time.sleep(1)

    # Criar o arquivo CSV e escrever o cabecalho
    with open('medidas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Date", "Time", "Tensao (V)", "Corrente (A)", "Potencia (W)", "Potencia (VA)", "Potencia (VAR)", "Fator de Potencia", "Angulo (Grau)", "Frequencia (Hz)", "Energia (Wh)", "Energia (Wh+)"])
        print(["Index", "Date", "Time", "Tensao (V)", "Corrente (A)", "Potencia (W)", "Potencia (VA)", "Potencia (VAR)", "Fator de Potencia", "Angulo (Grau)", "Frequencia (Hz)", "Energia (Wh)", "Energia (Wh+)"])
        prox_aq = datetime.now() + timedelta(hours=1)

        for x in range(750):
            now = datetime.now()
            if now <= prox_aq:
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                # Enviar comando e ler resposta
                response = read_sample("MEASURE:VAL?")
                values = response.split(',')

                # Converter valores para decimal
                values_decimal = convert_to_decimal(values)

                # Escrever valores no CSV
                row = [x, date_str, time_str] + values_decimal[:9] + values_decimal[9:12]
                writer.writerow(row)

                print(row)

                # Atualizar próximo horário de aquisicao
                #prox_aq = now + timedelta(seconds=1)
                time.sleep(1) # Espera 1 Segundo para pegar a proxima medida

    # Parar integracao
    write_sample("INTEGRATE:STOP")
    time.sleep(0.1)

# Configuracões iniciais do wattímetro
def configure_wattmeter():
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
        write_sample(command)
        time.sleep(0.1)

# Configurar wattímetro
configure_wattmeter()

# Executar medicões e salvar em CSV
main()

# Fechar conexao
instrument.close()
