import serial
import time

def configure_uart(port, baudrate=115200, timeout=1):
    """
    Configura a porta UART com os parametros especificados.
    """
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        print(f"[INFO] Porta {port} aberta com sucesso!")
        return ser
    except Exception as e:
        print(f"[ERRO] Nao foi possivel abrir a porta {port}: {e}")
        return None

def send_command(ser, command):
    """
    Envia um comando HCI pela UART e aguarda a resposta.
    """
    try:
        print(f"[ENVIO] Comando: {command.hex()}")
        ser.write(command)  # Envia o comando
        time.sleep(0.1)     # Pequeno atraso para garantir a resposta
        response = ser.read(ser.in_waiting or 100)  # Le a resposta disponivel
        if response:
            print(f"[RESPOSTA] {response.hex()}")
        else:
            print("[RESPOSTA] Nenhuma resposta recebida.")
        return response
    except Exception as e:
        print(f"[ERRO] Falha ao enviar o comando: {e}")
        return None

def close_uart(ser):
    """
    Fecha a porta UART de maneira segura.
    """
    if ser and ser.is_open:
        ser.close()
        print("[INFO] Porta UART fechada.")

if __name__ == "__main__":
    # Configuracao da porta UART     
    PORT = "COM10"  # Substitua pela sua porta COM
    BAUDRATE = 115200

    # Comandos HCI (modifique conforme necessario)
    commands = {
    # Comandos HCI basicos
    #"HCI_RESET": bytes([0x01, 0x03, 0x0C, 0x00]),
    #"HCI_READ_BD_ADDR": bytes([0x01, 0x09, 0x10, 0x00]),
    #"HCI_READ_LOCAL_VERSION_INFORMATION": bytes([0x01, 0x01, 0x10, 0x00]),
    #"HCI_READ_LOCAL_SUPPORTED_FEATURES": bytes([0x01, 0x03, 0x10, 0x00]),
    #"HCI_INQUIRY": bytes([0x01, 0x01, 0x04, 0x05, 0x33, 0x8B, 0x9E, 0x30]),

    # Comandos enviados pelo FCC_Assist
    "FCC_ASSIST_PRESET_001": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    "FCC_ASSIST_PRESET_002": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x05, 0x02, 0x00, 0x05, 0x00]),
    "FCC_ASSIST_PRESET_003": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x28, 0x05, 0x00, 0x0A, 0x00]),
    "FCC_ASSIST_PRESET_004": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x28, 0x00, 0x00, 0x0A, 0x01]),
    "FCC_ASSIST_PRESET_005": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x4E, 0x00, 0x01, 0x0A, 0x00]),

    # Comando customizado como exemplo
    "HCI_CUSTOM_COMMAND": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    
    "FCC_ASSIST_PRESET_001_MODIFIED": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00]),  # Exemplo de ajuste
    "FCC_ASSIST_PRESET_002_MODIFIED": bytes([0x01, 0x01, 0xFC, 0x06, 0x00, 0x05, 0x01, 0x00, 0x05, 0x00])   # Exemplo de ajuste

}


    # Abrir a porta UART
    ser = configure_uart(PORT, BAUDRATE)

    if ser:
        # Enviar comandos
        for cmd_name, cmd in commands.items():
            print(f"\n[TESTE] Enviando comando: {cmd_name}")
            send_command(ser, cmd)
        
        # Fechar a porta UART
        close_uart(ser)
