import csv, os

# Forma de abrir arquivo nativo do Python
teste = open('dados.csv')

# Utilizando módulo CSV para interpretar facilmente o arquivo CSV
teste2 = csv.reader(teste, delimiter=';', quotechar='"')

# Imprimindo leitura do módulo CSV
for line in teste2:
    print(', '.join(line))