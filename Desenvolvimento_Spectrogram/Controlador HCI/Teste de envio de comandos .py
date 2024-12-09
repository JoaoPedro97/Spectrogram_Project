import serial
import time

def configure_uart(port, baudrate=115200, timeout=1):
    """
    Configura a porta UART.
    """
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        print(f"Conectado a {port} com baudrate {baudrate}")
        return ser
    except Exception as e:
        print(f"Erro ao abrir a porta {port}: {e}")
        return None

def testar_tempo_resposta(ser):
    """
    Testa o tempo de resposta variando a frequencia de 0 a 79 (em hexa: 00 a 4F).
    """
    base_command = [0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00]
    for freq in range(0, 80):  # Loop de 0 a 79
        base_command[5] = freq  # Atualiza a frequencia (quinto byte do comando)
        command = bytes(base_command)
        
        try:
            # Envia o comando
            start_time = time.time()
            ser.write(command)
            
            # Aguarda resposta
            response = ser.read(ser.in_waiting or 100)
            end_time = time.time()
            
            # Calcula o tempo de resposta
            elapsed_time = (end_time - start_time) * 1000  # Tempo em ms
            
            # Exibe o resultado
            print(f"Frequencia: {freq} (Hex: {freq:02X}), Tempo de resposta: {elapsed_time:.2f} ms")
            if response:
                print(f"Resposta: {response.hex()}")
            else:
                print("Sem resposta")
        except Exception as e:
            print(f"Erro ao enviar comando para frequencia {freq}: {e}")

if __name__ == "__main__":
    # Configuracao inicial
    porta = "COM10"  # Substituir pela porta correta
    baudrate = 115200
    
    # Conecta na porta
    ser = configure_uart(porta, baudrate)
    if ser:
        testar_tempo_resposta(ser)
        ser.close()
        print("Teste concluido. Porta fechada.")
    else:
        print("Nao foi possivel conectar a porta.")



#
#import serial
#import time
#
#def configure_uart(port, baudrate=115200, timeout=1):
#    """
#    Configura a porta UART.
#    """
#    try:
#        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
#        print(f"Conectado a {port} com baudrate {baudrate}")
#        return ser
#    except Exception as e:
#        print(f"Erro ao abrir a porta {port}: {e}")
#        return None
#
#def enviar_comandos_sem_retorno(ser):
#    """
#    Envia comandos variando a frequencia de 0 a 79 (em hexa: 00 a 4F) sem aguardar retorno.
#    """
#    base_command = [0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00]
#    for freq in range(0, 80):  # Loop de 0 a 79
#        base_command[5] = freq  # Atualiza a frequencia (quinto byte do comando)
#        command = bytes(base_command)
#        
#        try:
#            # Envia o comando
#            ser.write(command)
#            print(f"Comando enviado: Frequencia {freq} (Hex: {freq:02X})")
#            
#            # Aguarda um pequeno intervalo antes de enviar o proximo comando
#            time.sleep(0.05)  # 50 ms entre os comandos
#        except Exception as e:
#            print(f"Erro ao enviar comando para frequencia {freq}: {e}")
#
#if __name__ == "__main__":
#    # Configuracao inicial
#    porta = "COM10"  # Substituir pela porta correta
#    baudrate = 115200
#    
#    # Conecta na porta
#    ser = configure_uart(porta, baudrate)
#    if ser:
#        enviar_comandos_sem_retorno(ser)
#        ser.close()
#        print("Comandos enviados. Porta fechada.")
#    else:
#        print("Nao foi possivel conectar a porta.")
#