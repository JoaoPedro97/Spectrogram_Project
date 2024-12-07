#import serial
#
#def monitorar_porta(porta="COM10", baudrate=115200):
#    try:
#        # Abre a porta espelhada para monitoramento
#        with serial.Serial(port=porta, baudrate=baudrate, timeout=1) as ser:
#            while True:
#                if ser.in_waiting > 0:
#                    dados_recebidos = ser.read(ser.in_waiting).decode(errors='ignore')
#                    print(f"Dados recebidos: {dados_recebidos}")
#
#    except serial.SerialException as e:
#        print(f"Erro ao abrir a porta serial: {e}")
#
## Exemplo de uso
#monitorar_porta(porta="COM10", baudrate=115200)

import serial.tools.list_ports

def listar_portas():
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        print(f"Porta: {porta.device} - Descricao: {porta.description}")

listar_portas()
