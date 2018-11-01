import main
import matplotlib.pyplot as plt
import numpy as np

de = main.main('data.csv')
# Lucro da venda por produto
de.profit(by=de.PRODUCT)
# Lucro da venda por região
de.profit(by=de.REGION)

# Lucro de uma determinada região
de.profit(by=de.REGION) # Usar o de cima

# Lucro de uma determinada região por produto
de.profit(by=de.REGION, split=True)

# Região mais lucrativa (SEM gráfico)
de.mostProfitable(de.profit(by=de.REGION))
# Produto mais lucrativo (SEM gráfico)
de.mostProfitable(de.profit(by=de.PRODUCT))

profitByProduct = de.profit(by=de.PRODUCT)
profitByRegion = de.profit(by=de.REGION)
objects = tuple([k for k,v in profitByRegion.items()])
y_pos = np.arange(len(objects))
profits = [v['totalProfit'] for k,v in profitByRegion.items()]

plt.bar(y_pos, profits, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Lucro')
plt.title('Lucro por produto')

plt.show()
plt.close()

# =======================

profitByRegionByProduct = de.profit(by=de.REGION, split=True)
regions = tuple(list(profitByRegionByProduct.keys()))
y_pos = np.arange(len(regions))
prodData = {}
for k,v in profitByRegionByProduct.items():
    for prod, value in v.items():
        if (prodData.setdefault(prod, (value['totalProfit'],)) != (value['totalProfit'],)):
            prodData[prod] = prodData[prod] + (value['totalProfit'],)

plt.subplots()
bar_width = 0.2
opacity = 0.8
barQnt = len(prodData)
totalWidth = barQnt*bar_width
start = (totalWidth/2) * -1

for prodName, data in prodData.items():
    plt.bar(y_pos + start, data, bar_width, alpha=opacity, label=prodName)
    start += bar_width

plt.xlabel('Regiões')
plt.ylabel('Lucro')
plt.title('Lucro por região por produto')
plt.xticks(y_pos + (-bar_width/2), regions)
plt.legend()

plt.tight_layout()
plt.show()
plt.close()
