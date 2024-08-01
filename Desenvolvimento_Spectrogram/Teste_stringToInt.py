def string_para_inteiro(s):
    try:
        return int(s)
    except ValueError:
        print(f"Erro: '{s}' nao e uma string numerica valida.")
        return None

# Exemplo de uso
string_num = 'a'
numero = string_para_inteiro(string_num)
print(numero)  # Output: 1
