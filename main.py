import csv, os
from classes import DataExtractor

def main(arqPath, prodCostFile):
    print(arqPath)
    # Forma de abrir arquivo nativo do Python
    if type(arqPath) == type(''): teste = open(arqPath)
    else: teste = arqPath

    # Utilizando módulo CSV para interpretar facilmente o arquivo CSV
    teste2 = csv.reader(teste, delimiter=';', quotechar='"')

    dados = None
    # Imprimindo leitura do módulo CSV
    for num, line in enumerate(teste2):
        #print(', '.join(line))
        if num == 0:
            dados = DataExtractor(line, prodCostFile)
        else:
            dados.setRegister(line)
    return dados
