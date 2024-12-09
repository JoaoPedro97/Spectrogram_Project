import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports

# Funcao para listar portas COM disponiveis
def listar_portas():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Funcao para enviar comando via UART
def enviar_comando():
    global ser
    comando = entrada_comando.get()
    if not comando:
        messagebox.showwarning("Aviso", "Digite um comando em hexadecimal!")
        return

    try:
        # Converter o comando de string hexadecimal para bytes
        comando_bytes = bytes.fromhex(comando)
        ser.write(comando_bytes)
        resposta = ser.read(ser.in_waiting or 100)  # Le ate 100 bytes ou o que estiver disponivel
        texto_resposta.config(state="normal")
        texto_resposta.insert(tk.END, f"Enviado: {comando}\n")
        texto_resposta.insert(tk.END, f"Resposta: {resposta.hex()}\n\n")
        texto_resposta.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao enviar comando: {e}")

# Funcao para conectar na porta UART
def conectar():
    global ser
    porta = combo_porta.get()
    baudrate = int(combo_baudrate.get())
    try:
        ser = serial.Serial(porta, baudrate=baudrate, timeout=1)
        messagebox.showinfo("Sucesso", f"Conectado a porta {porta} com baud rate {baudrate}")
    except Exception as e:
        messagebox.showerror("Erro", f"Nao foi possivel abrir a porta {porta}: {e}")

# Configuracao inicial do Tkinter
app = tk.Tk()
app.title("MVP - Teste de Comandos UART")
app.geometry("500x400")

# Selecao de porta COM
frame_conexao = tk.Frame(app)
frame_conexao.pack(pady=10)

tk.Label(frame_conexao, text="Porta COM:").pack(side=tk.LEFT, padx=5)
combo_porta = ttk.Combobox(frame_conexao, values=listar_portas(), width=10)
combo_porta.pack(side=tk.LEFT, padx=5)
combo_porta.set("Selecione")

tk.Label(frame_conexao, text="Baud Rate:").pack(side=tk.LEFT, padx=5)
combo_baudrate = ttk.Combobox(frame_conexao, values=["9600", "19200", "38400", "57600", "115200"], width=10)
combo_baudrate.pack(side=tk.LEFT, padx=5)
combo_baudrate.set("115200")

btn_conectar = tk.Button(frame_conexao, text="Conectar", command=conectar)
btn_conectar.pack(side=tk.LEFT, padx=5)

# Entrada de comando
frame_comando = tk.Frame(app)
frame_comando.pack(pady=10)

tk.Label(frame_comando, text="Comando Hexadecimal:").pack(side=tk.LEFT, padx=5)
entrada_comando = tk.Entry(frame_comando, width=30)
entrada_comando.pack(side=tk.LEFT, padx=5)

btn_enviar = tk.Button(frame_comando, text="Enviar", command=enviar_comando)
btn_enviar.pack(side=tk.LEFT, padx=5)

# area de exibicao de resposta
frame_resposta = tk.Frame(app)
frame_resposta.pack(pady=10, fill="both", expand=True)

texto_resposta = tk.Text(frame_resposta, wrap="word", height=10, state="disabled")
texto_resposta.pack(fill="both", expand=True, padx=10, pady=10)

# Loop principal do Tkinter
app.mainloop()
