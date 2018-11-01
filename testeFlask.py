import os
import flask
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

"""
to run:
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run

Style:
Criar dict com os estilos, onde as keys serão como se fossem classes e você pode chamar dentro de style=
"""

server = flask.Flask(__name__)
cssFiles = ['fatecStyle.css']
external_stylesheets = [('/static/' + cssFile) for cssFile in cssFiles]

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

@server.route('/') # Bem-vindo e carregar arquivo CSV
def hello():
	return flask.render_template('template.html',
                           titleComplexChart='Gráfico Complexo',
                           complexGraph='Olá!')

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
