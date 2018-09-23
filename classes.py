from datetime import date
# Esse dicionário auxilia na passagem das abreviações
# de meses para a representação em numeral
monthToNum = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'out': 10,
    'nov': 11,
    'dez': 12
}

class Data:
    """
    /**/
    """
    def __init__(self, headerList):
        self.headerRaw = headerList
        self.colsData = self.__handleHeader()
        self.registerList = []

    def __handleHeader(self):
        colsData = {}
        for num, col in enumerate(self.headerRaw):
            finalWord = ''
            # Removendo espaços e mantendo primeira palavra lowCase
            # e as demais com a primeira letra maiúscula
            for num2, word in enumerate(col.split()):
                finalWord += word.lower() if num2 == 0 else word.lower().replace(word[0].lower(), word[0].upper())
            # Criando dados de cada nome de coluna
            colData = {
                'colName': self.headerRaw[num],
                'colCod': finalWord
            }
            colsData.setdefault(num + 1, colData)
        return colsData

    def __checkColNum(self, registerRaw):
        """
        Validação para o número de colunas antes de adicionar o registro
        :return: Boolean - True se estiver com o número correto e False do contrário
        """
        return len(self.headerRaw) == len(registerRaw)

    def setRegister(self, registerRaw):
        if self.__checkColNum(registerRaw):
            self.registerList.append(Register(registerRaw))
        else:
            # tratar erro aqui
            pass

    def getColNameByNum(self, num):
        for numCol, data in self.colsData.items():
            if numCol == num:
                return data['colName']

    def getColNameByCod(self, cod):
        for numCol, data in self.colsData.items():
            if data['colCod'] == cod:
                return data['colName']

    def getColNumByCod(self, cod):
        for numCol, data in self.colsData.items():
            if data['colCod'] == cod:
                return numCol

class Register:
    """
    /**/
    """

    def __init__(self, registerRaw):
        self.id = int(registerRaw[0])
        self.storeNo = int(registerRaw[1])
        self.selesRegion = str(registerRaw[2])
        self.itemNo = int(registerRaw[3])
        self.itemDescription = str(registerRaw[4])
        self.unitPrice = float(registerRaw[5].replace('$','').replace(',','.'))
        self.unitsSold = int(registerRaw[6])
        self.weekEnding = self.__handleDate(registerRaw[7])

    def __handleDate(self, dateString):
        return date(*tuple(
            [monthToNum[value] if pos==1 else
             (int('20' + value) if pos==0 else
              int(value))
             for pos, value in enumerate(reversed(dateString.split('/')))]
        ))

    def teste(self):
        pass