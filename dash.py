import dash, base64, io
from dash.dependencies import Input, Output, Event, State
import dash_html_components as html
import dash_core_components as dcc
import main

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css'
    ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

salles = None
costs  = None

title = html.H1('Salles Analyzer')
# O arquivo é carregado em binário
upload = dcc.Upload(
    id='upload',
    children=html.Div([
        'Arraste aqui ou ',
        html.A('Selecione o arquivo')
    ]),
    style={
        'width': '98%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    }, multiple=True)
dropdown = dcc.Dropdown(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    multi=True,
    value="MTL"
)

app.layout = html.Div([
    title,
    upload,
    html.Div(id='output-data-upload', className='row')
    #html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])

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

def register_files(contents, filename, date):
    global salles, costs
    if not contents==None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        CSVfile = io.StringIO(decoded.decode('utf-8'))

        if 'salles' in filename and salles==None: salles = CSVfile
        elif 'costs' in filename and costs==None: costs = CSVfile

        return None

def genarate_graphs():
    if salles and costs:
        results = []
        dados = main.main(salles, costs)
        profitByRegionByProduct = dados.profit(by=dados.REGION, split=True)
        # Lucro da venda por produto
        profitByProduct = dados.profit(by=dados.PRODUCT)
        # Lucro da venda por região
        profitByRegion = dados.profit(by=dados.REGION)
        # Região mais lucrativa (SEM gráfico)
        mostProfitableRegion = dados.mostProfitable(dados.profit(by=dados.REGION))
        # Produto mais lucrativo (SEM gráfico)
        mostProfitableProduct = dados.mostProfitable(dados.profit(by=dados.PRODUCT))

        results.append(
            html.Div(
                [html.Div(
                    [html.P('Região mais lucrativa: ', className='result-title'),
                     html.P(list(mostProfitableRegion)[0], className='result-value')],
                    id='mostProfitableRegion',
                    className='col'),
                html.Div(
                    [html.P('Produto mais lucrativo: ', className='result-title'),
                     html.P(list(mostProfitableProduct)[0], className='result-value')],
                    id='mostProfitableProduct',
                    className='col')],
                className='row'
            )
        )

        results.append(dcc.Graph(id='profitByRegionByProduct',
            figure={
                'data': convertInfo(profitByRegionByProduct, 'complex'),
                'layout': {
                    'title': 'Lucro dos produtos por região'
                }
            })
        )

        results.append(dcc.Graph(id='profitByProduct',
            figure={
                'data': convertInfo(profitByProduct),
                'layout': {
                    'title': 'Lucro por produto'
                }
            })
        )

        results.append(dcc.Graph(id='profitByRegion',
            figure={
                'data': convertInfo(profitByRegion),
                'layout': {
                    'title': 'Lucro por região'
                }
            })
        )

        if len(results)>2:
            class_choice = 'col s12 m6 l6'
        elif len(results) == 2:
            class_choice = 'col s12 m6 l6'
        else:
            class_choice = 'col s12'

        elements = [html.Div([res], className=class_choice) for res in results]

        return True, elements
    else: return False, None


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload', 'contents')],
              [State('upload', 'filename'),
              State('upload', 'last_modified')])
def recieve_files(listContents, listNames, listDates):
    if listContents is not None:
        children = [
            register_files(c, n, d) for c, n, d in
            zip(listContents, listNames, listDates)]
    worked, graphs = genarate_graphs()
    if worked:
        return graphs

"""register_files(content_salles, list_of_names, list_of_dates)
    register_files(list_of_contents, list_of_names, list_of_dates)
    worked, graph = genarate_graph()
    if worked: return graph"""

"""@app.callback(Output('p_section', 'children'), events=[Event('button', 'click')])
def update_output():
    fig = dcc.Graph(
        id='example',
        figure={
            'data': [{
                'y': [1, 5, 3],
                'type': 'bar'
            }]
        }
    )
    fig2 = dcc.Graph(
        id='example-1',
        figure={
            'data': [{
                'y': [1, 5, 3],
                'type': 'bar'
            }]
        }
    )
    return [fig, fig2]"""

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')