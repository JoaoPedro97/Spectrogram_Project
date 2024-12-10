from RsInstrument import RsInstrument

# Configuracao basica
INSTRUMENT_IP = "192.168.0.126"  # IP do analisador
TIMEOUT = 30000  # Timeout em ms

# Conexao com o instrumento
def connect_to_instrument(ip_address):
    try:
        instr = RsInstrument(f"TCPIP::{ip_address}::INSTR", True, False)
        instr.visa_timeout = TIMEOUT
        print("Conexao estabelecida com:", instr.query_str("*IDN?"))
        return instr
    except Exception as e:
        print("Erro ao conectar ao instrumento:", e)
        return None

# Configuracao do analisador
def configure_analyzer(instr):
    try:
        commands = [
            "*RST",  # Reset do instrumento
            "SYST:DISP:UPD OFF",  # Desativa atualizacao automatica para configuracao
            "DET RMS",  # Configura o detector para RMS
            "DISP:WIND:TRAC:MODE AVER",  # Configura o traco para Average
            "CALC:MATH:MODE LIN",  # Configura a media para linear
            "SENS:BAND:RES 1 MHz",  # Configura RBW para 1 MHz
            "SENS:BAND:VID 3 MHz",  # Configura VBW para 3 MHz
            "FREQ:SPAN 30 MHz",  # Configura o span para 30 MHz
            "FREQ:CENT 5240 MHz",  # Configura a frequencia central para 5240 MHz
            "SENS:SWE:COUN 100",  # Configura o numero de varreduras para 100
            "INIT:CONT OFF",  # Configura para Single Sweep
            "SYST:DISP:UPD ON",  # Reativa a atualizacao do display
            "INIT:IMM"  # Inicia a medicao
        ]

        for cmd in commands:
            instr.write_str(cmd)
            print(f"Comando enviado: {cmd}")

        print("Configuracao concluida com sucesso!")
    except Exception as e:
        print("Erro na configuracao do analisador:", e)

# Execucao principal
def main():
    instrument = connect_to_instrument(INSTRUMENT_IP)
    if instrument:
        configure_analyzer(instrument)
        instrument.close()
        print("Instrumento desconectado.")

if __name__ == "__main__":
    main()
