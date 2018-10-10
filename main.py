import csv, os
from classes import DataExtractor

def main(arqPath):
    print(arqPath)
    # Forma de abrir arquivo nativo do Python
    teste = open(arqPath)

    # Utilizando módulo CSV para interpretar facilmente o arquivo CSV
    teste2 = csv.reader(teste, delimiter=';', quotechar='"')

    dados = None
    # Imprimindo leitura do módulo CSV
    for num, line in enumerate(teste2):
        print(', '.join(line))
        if num == 0:
            dados = DataExtractor(line)
        else:
            dados.setRegister(line)
    #return dados
