import os
import flask
import dash
import plotly, json
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from . import main

"""
to run:
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run

Style:
Criar dict com os estilos, onde as keys serão como se fossem classes e você pode chamar dentro de style=
"""

server = flask.Flask(__name__)
cssFiles = ['fatecStyle.css', 'styleIndex.css']
external_stylesheets = [('/static/' + cssFile) for cssFile in cssFiles]
print(external_stylesheets)

app = dash.Dash(__name__, server=server, url_base_pathname='/dummypath/', external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    #dcc.Input(id='input', value='Enter something...', type='text'),
    #html.Div(id='output', style={'width': '50%'})
    html.H1('Dash tutorials'),
    dcc.Graph(id='exemple', style={'width': '50%'},
        figure={
            'data': [
                {'x': [1,2,3,4,5], 'y': [4,6,9,3,5], 'type':'bar', 'name': 'Computers'},
                {'x': [1,2,3,4,5], 'y': [8,5,4,2,6], 'type':'bar', 'name': 'Mouses'}
                ],
            'layout': {
                'title': 'TESTE'
            }
        })
    ], className='btn-fatec')

"""@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(input_data):
    return 'Input: {}'.format(input_data)"""

def loadCSS(file):
    with open(file) as css:
        return css.read()

def convertInfo(raw, type='simple'):
    dataList = []
    
    regions = [k for k in raw.keys()]
    prodData = {}
    if type == 'complex':
        for k,v in raw.items():
            for prod, value in v.items():
                if (prodData.setdefault(prod, (value['totalProfit'],)) != (value['totalProfit'],)):
                    prodData[prod] = prodData[prod] + (value['totalProfit'],)
        for prodName, data in prodData.items():
            dataList.append({'x': regions, 'y': list(data), 'type':'bar', 'name': prodName})
    else:
        tempData = []
        for region in regions:
            tempData.append(raw[region]['totalProfit'])
        dataList.append({'x': regions, 'y': tempData, 'type':'bar'})
    return dataList

@server.route('/') # Bem-vindo e carregar arquivo CSV
def hello():
    dados = main.main('data.csv')

    profitByRegionByProduct = dados.profit(by=dados.REGION, split=True)
    # Lucro da venda por produto
    profitByProduct = dados.profit(by=dados.PRODUCT)
    # Lucro da venda por região
    profitByRegion = dados.profit(by=dados.REGION)
    # Região mais lucrativa (SEM gráfico)
    mostProfitableRegion = dados.mostProfitable(dados.profit(by=dados.REGION))
    # Produto mais lucrativo (SEM gráfico)
    mostProfitableProduct = dados.mostProfitable(dados.profit(by=dados.PRODUCT))

    
    graphs = {
        'data': convertInfo(profitByRegionByProduct, 'complex'),
        'layout': {'barmode': 'group'}
    }
    simpleGraphs = [
        {
            'id': 1,
            'title': 'Lucro de venda por produto',
            'data': json.dumps({'data': convertInfo(profitByProduct)}, cls=plotly.utils.PlotlyJSONEncoder)
        },
        {
            'id': 2,
            'title': 'Lucro de venda por região',
            'data': json.dumps({'data': convertInfo(profitByRegion)}, cls=plotly.utils.PlotlyJSONEncoder)
        }
    ]
    return flask.render_template('template.html',
                           titleComplexChart='Puta teste',
                           complexGraph=json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder),
                           simpleGraphs=simpleGraphs,
                           item1='Região mais lucrativa',
                           item1data=list(mostProfitableRegion)[0],
                           item2='Produto mais lucrativo',
                           item2data=list(mostProfitableProduct)[0])

@server.route('/dash')
def dashPage():
    return app.index()

#return str(os.listdir())
#with open('template.htm') as template:
#    cache = template.read()
#    return cache.format(
#            fatecCSS=loadCSS('fatecStyle.css')
#        )
#@app.route('/fatecCSS.css')
#def 
