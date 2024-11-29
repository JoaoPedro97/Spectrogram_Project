from RsInstrument import RsInstrument

# Configurar o IP do ESR
esr_ip = "192.168.0.126"

# Conectar ao instrumento
instr = RsInstrument(f'TCPIP::{esr_ip}::INSTR', True, False)

try:
    # Configurar o formato BMP e destino
    instr.write_str('HCOP:DEV:LANG BMP')  # Formato BMP
    instr.write_str('HCOP:DEST "MMEM"')  # Destino: Memória interna

    # Definir o caminho do arquivo na memória interna
    instr.write_str('MMEM:NAME "C:\\Temp\\esr_screenshot.bmp"')

    # Criar o diretório, se necessário
    instr.write_str('MMEM:MDIR "C:\\Temp"')

    # Capturar a tela
    instr.write_str('HCOP:IMM')

    # Transferir o arquivo para o computador
    local_path = "C:\\Users\\Public\\Documents\\esr_screenshot.bmp"
    instr.query_bin_block_to_file('MMEM:DATA? "C:\\Temp\\esr_screenshot.bmp"', local_path)

    print(f"Print salvo em: {local_path}")

except Exception as e:
    print(f"Erro ao capturar o print: {e}")

finally:
    instr.close()
