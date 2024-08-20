import pandas as pd
import matplotlib.pyplot as plt

file_path = 'medicoes.csv'
df = pd.read_csv(file_path, delimiter=';')

plt.figure(figsize=(10, 6))
plt.plot(df['date'] + ' ' + df['Hora'], df['Tensao (V)'], marker='o')
plt.title('Tensao ao Longo do Tempo')
plt.xlabel('Data e Hora')
plt.ylabel('Tensao (V)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
