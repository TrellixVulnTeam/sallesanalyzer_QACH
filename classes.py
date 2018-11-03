import csv,os
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
    def __init__(self, headerList, prodCostFile):
        self.__productsCost = self.__getProductsCost(prodCostFile)
        self.headerRaw = headerList
        self.colsData = self.__handleHeader()
        self.registerList = []

    def __getProductsCost(self, prodCostFile):
        prodCost = {}
        with (open(os.path.join(os.getcwd(),'prodTable.csv')) if not prodCostFile else prodCostFile) as prodTableCSV:
            prodCostList = csv.reader(prodTableCSV, delimiter=';', quotechar='"')
            for line, value in enumerate(prodCostList, 1):
                if(line!=1):
                    product, cost = value
                    prodCost.setdefault(product, cost)
        return prodCost

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
            self.registerList.append(Register(registerRaw, self.__productsCost))
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

    def __init__(self, registerRaw, unitCost):
        self.id = int(registerRaw[0])
        self.storeNo = int(registerRaw[1])
        self.salesRegion = str(registerRaw[2])
        self.itemNo = int(registerRaw[3])
        self.itemDescription = str(registerRaw[4])
        self.unitPrice = float(registerRaw[5].replace('$','').replace(',','.'))
        self.unitCost = float(unitCost[self.itemDescription])
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

class DataExtractor(Data):

    ALL    = 0
    STORE  = 1
    REGION = 2
    DATE   = 3
    TOTAL_SALES_VALUE = 10
    TOTAL_SOLD_ITEMS  = 20
    PRODUCT           = 30


    def sSortRegisters(self, by=STORE):
        if(by==self.STORE):
            biggerPos = self.registerList[0].storeNo
            for i, register in enumerate(self.registerList):
                if(register.storeNo):
                    pass

    def __findMostSold(self, by):
        mostSold = {}
        for register in self.registerList:
            mostSold.setdefault(register.__getattribute__(by), {})
            if (mostSold[register.__getattribute__(by)].setdefault(register.itemDescription,
                                                      register.unitsSold) != register.unitsSold):
                mostSold[register.__getattribute__(by)][register.itemDescription] += register.unitsSold
        for store, value in mostSold.items():
            auxP = ''
            auxV = ''
            for product, units in value.items():
                if (not auxP):
                    auxP = product
                    auxV = units
                if (units > value[auxP]):
                    auxP = product
                    auxV = units
            mostSold[store] = {auxP: auxV}
        return mostSold

    def mostSoldProduct(self, by=ALL):
        """
        Retornar dicionario com os dados do 'vencedor'
        :param by: Int - Critério de divisão
        :return: Dict - Dicionário com o 'vencedor'
        """
        if(by==self.ALL):
            mostSold = {}
            for register in self.registerList:
                if (mostSold.setdefault(register.itemDescription, register.unitsSold) != register.unitsSold):
                    mostSold[register.itemDescription] += register.unitsSold
            pass
            return mostSold
        elif(by==self.STORE):
            return self.__findMostSold('storeNo')
        elif(by==self.REGION):
            return self.__findMostSold('salesRegion')
        elif(by==self.DATE):
            return self.__findMostSold('weekEnding')
        else: raise Exception

    def __findProfitsLowLevel(self, dic, rg):
        model = {'totalProfit': 0, 'unitsSold': 0}
        dic.setdefault(rg.itemDescription, model)
        unitProfitValue = rg.unitPrice - rg.unitCost
        dic[rg.itemDescription]['unitsSold'] += rg.unitsSold
        dic[rg.itemDescription]['totalProfit'] = unitProfitValue * dic[rg.itemDescription]['unitsSold']
        return dic

    def __findProfits(self, by, split=False):
        productProfit = {}
        of = 'itemDescription'
        if by == of:
            for register in self.registerList:
                productProfit = self.__findProfitsLowLevel(productProfit, register)
        else:
            for register in self.registerList:
                if by != of: productProfit.setdefault(register.__getattribute__(by), {})
                productProfit[register.__getattribute__(by)] = self.__findProfitsLowLevel(
                    productProfit[register.__getattribute__(by)], register)
            for k, v in productProfit.items():
                model = {'totalProfit': 0, 'unitsSold': 0}
                if not split:
                    for product, data in v.items():
                        model['totalProfit'] += data['totalProfit']
                        model['unitsSold'] += data['unitsSold']
                    productProfit[k] = model
        return productProfit

    def profit(self, by=PRODUCT, split=False):
        """
        Retorna o lucro por produto ou por região. O split separa o lucro por produto em cada região

        :param by: int - Escolher mostrar o lucro por PRODUTO ou por REGIÃO
        :param split: boolean - Se True, separa o lucro por produto na opção por REGIÃO
        :return: Dict - Dicionário com o resultado
        """
        if(by==self.PRODUCT):
            return self.__findProfits('itemDescription')
        elif(by==self.REGION):
            return self.__findProfits('salesRegion', split=split)

    def __findMoreProfitable(self, by):
        pass

    def mostProfitable(self, data):
        theMost = {}
        for k, v in data.items():
            if not theMost: theMost = {k}
            else:
                for key in theMost:
                    if data[k]['totalProfit'] > data[key]['totalProfit']:
                        theMost = {k}
                        break
                    elif data[k]['totalProfit'] == data[key]['totalProfit']:
                        theMost.add(k)
                        break
        return theMost

# Maior em quantidade
# Maior em valor
# LUCRO