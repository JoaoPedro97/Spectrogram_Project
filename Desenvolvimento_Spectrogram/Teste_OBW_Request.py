#from RsInstrument import RsInstrument
#import time
#
## Configurar o IP do ESR
#esr_ip = "192.168.0.126"
#
## Conectar ao instrumento
#instr = RsInstrument(f'TCPIP::{esr_ip}::INSTR', True, False)
#
#try:
#    instr.write_str("INIT:IMM")
#    # Loop ate o FSMR sinalizar que esta pronto
#    while int(instr.query_str("*ESR?")) != 0:
#        time.sleep(0.1)  # Verificar a cada 100ms
#        print(instr.query_str("*ESR?"))
#
## Consultar os resultados
#    obw_result = instr.query_str("CALC:MARK:FUNC:POW:RES? OBW")
#    print("Largura de banda ocupada:", obw_result)
#    
#    
#    instr.write_str("CALC:MARK:FUNC:POW:SEL OBW")
#    instr.write_str("SENS:POW:BWID 99PCT")
#    instr.write_str("INIT:IMM")  # Iniciar medicao
#    
#    # Esperar pelo termino da medicao
#    instr.query_str("*OPC?")
#    
#    # Consultar o resultado
#    obw_result = instr.query_str("CALC:MARK:FUNC:POW:RES? OBW")
#    #print("Largura de banda ocupada:", obw_result)
#    print("Potencia:", obw_result)
#
#
#except Exception as e:
#    print(f"Erro ao capturar o print: {e}")
#
#finally:
#    instr.close()


#import time
#
#def measure_execution_time(func, *args, **  ):
#    # Captura o tempo de inicio
#    start_time = time.time()
#    
#    # Executa a funcao com os argumentos fornecidos
#    func(*args, **kwargs)
#    
#    # Captura o tempo de termino
#    end_time = time.time()
#    
#    # Calcula o tempo total de execucao
#    execution_time = end_time - start_time
#    
#    # Retorna o tempo de execucao formatado
#    print(f"Tempo de execucao: {execution_time:.3f} segundos")
#    return execution_time
#
## Exemplo de funcao a ser testada
#def sample_function():
#    # Simulando um processo com um atraso de 2 segundos
#    time.sleep(2)
#    print("Funcao executada!")
#
## Medindo o tempo de execucao da funcao `sample_function`
#measure_execution_time(sample_function)





##FUNCIONA! 
#from RsInstrument import RsInstrument
#
#def wait_for_sweep_completion():
#    try:
#        # Conecta ao analisador de espectro no IP especificado
#        ip_address = "192.168.0.111"
#        instr = RsInstrument(f"TCPIP::{ip_address}::INSTR", True, False)
#        
#        # Configura o numero de varreduras (Sweep Count)
#        sweep_count = 100
#        instr.write_str("INIT:CONT OFF; :INIT")
#        instr.write_str(f"SENS:SWE:COUN {sweep_count}")
#        
#        # Inicia a medicao
#        instr.write_str("INIT:IMM")
#        instr.write_str("INIT;*WAI")
#        
#        # Aguarda a conclusao de todas as medidas
#        print("Esperando o Sweep concluir todas as medidas...")
#        opc_response = instr.query_str("*OPC?")  # Garante que todas as varreduras terminem
#        
#        # Verifica se a resposta foi recebida
#        if opc_response.strip() == "1":
#            print(f"Todas as {sweep_count} medidas foram concluidas com sucesso.")
#        else:
#            print("Erro ao concluir as medidas.")
#        
#    except Exception as e:
#        print(f"Erro: {e}")
#    finally:
#        # Fecha a conexao com o instrumento
#        instr.close()
#
## Chama a funcao
#wait_for_sweep_completion()



#import tkinter as tk
#
#def toggle_checkbox():
#    # Verifica o estado do primeiro checkbox
#    if master_checkbox_var.get():
#        dependent_checkbox.config(state="disabled")  # Desabilita o segundo checkbox
#    else:
#        dependent_checkbox.config(state="normal")  # Habilita o segundo checkbox
#
## Criando a janela principal
#root = tk.Tk()
#root.geometry("300x200")
#root.title("Exemplo de Checkbutton Dinamico")
#
## Variavel para o checkbox principal
#master_checkbox_var = tk.BooleanVar()
#
## Checkbutton principal que controla o outro
#master_checkbox = tk.Checkbutton(
#    root, text="Desabilitar o outro checkbox", variable=master_checkbox_var, command=toggle_checkbox
#)
#master_checkbox.pack(pady=10)
#
## Variavel para o checkbox dependente
#dependent_checkbox_var = tk.BooleanVar()
#
## Checkbutton dependente
#dependent_checkbox = tk.Checkbutton(
#    root, text="Checkbox Dependente", variable=dependent_checkbox_var
#)
#dependent_checkbox.pack(pady=10)
#
## Iniciando o loop principal do Tkinter
#root.mainloop()





import re

string = "ab12c34def567342432432890gh1234"
apenas_numeros = re.findall(r'\d', string)  # Lista com todos os dígitos
oito_digitos = ''.join(apenas_numeros[:8])  # Pega os primeiros 8
print(oito_digitos)  # Saída: 12345678