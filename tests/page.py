import dash
import dash_core_components as dcc
import dash_html_components as html
import main

app = dash.Dash()

dados = main.main('data.csv')
profitByRegionByProduct = dados.profit(by=dados.REGION, split=True)

regions = [k for k in profitByRegionByProduct.keys()]
prodData = {}
for k,v in profitByRegionByProduct.items():
    for prod, value in v.items():
        if (prodData.setdefault(prod, (value['totalProfit'],)) != (value['totalProfit'],)):
            prodData[prod] = prodData[prod] + (value['totalProfit'],)

dataList = []
for prodName, data in prodData.items():
    dataList.append({'x': regions, 'y': list(data), 'type':'bar', 'name': prodName})

app.layout = html.Div(children=[
    html.H1('Dash tutorials'),
    dcc.Graph(id='exemple',
        figure={
            'data': dataList,
            'layout': {
                'title': 'Lucro de regiões por produto'
            }
        })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)