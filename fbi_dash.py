#!/usr/bin/env python3
#Steven A Vasquez
#Megan Kelly
#Date Created: 04/06/2020
#Last Updated: 04/27/2020

#This script is used to produce a dashboard displaying violent crimes in the United States since 1999

#This uses Dash/plotly 

#To use this script python fbi_dash.py

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import base64
#import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#sets up the application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Import data 
df = pd.read_csv('clean_crime')
#Drop unneeded column
df = df.drop('Unnamed: 0',axis=1)
#Will transpose the original dataset besides Year and Population for call backs
dff = df.melt(id_vars=["Year", "Population"])
#Used to create dropdown menus 
# second lets the double interactive feature work, if population is an option, no graphic appears 
ddf = df.loc[:, df.columns != 'Year']
available_indicators = list(ddf.columns)
available_indicators2 = list(x for x in ddf.columns if x != 'Population')
#Data frame for population graph callback
pop_df = df.melt(id_vars=["Year"])

# To read in the saved image to be displayed at the top
image_filename = 'FBI-logo.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


#This code was taken from Plotly tutorial, very useful way of creating a table showcasing the data 
def generate_table(dataframe, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

#Scatter plot of population of the United States and a separate one of the violent crime rate in the US
population=go.Scatter(x=list(df['Year']),y = list(df['Population']),name = 'Population of United States')
violent_crime=go.Scatter(x=list(df['Year']), y=list(df['Violent_Crime']),name='Violent Crimes')

#Create a list of data that will be plotted
data = [population,violent_crime]
#Create the layout of the graph 
layout = dict(title = 'Population', showlegend = False)
#What is referenced when creating the graphs
fig = dict(data =data, layout=layout)



#Create the lay out of the application
app.layout = html.Div(children=[
	html.H1(children='FBI Violent Crime Data', style={'textAlign': 'center'}),
    html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))], style={'textAlign': 'center'}),
	html.H2(children='Welcome to our website!', style={'textAlign': 'center'}),
	html.H3(children='The interactive graphs below visualize the violent crimes committed in the United States over the past 20 years according to the FBI records.  Graphs can be customized via the pull down menus for further data analysis.', style={'textAlign': 'center'}),
	html.Div(children=''' Please note at the bottom of this site we have provided a table showcasing the data.  Additionally there is a link to the website containing the orignal data set.  The website explains the missing information in reference to certain crimes such as rape and arson because of new revisions of the crime's definition.  If you have further inquires about the data you should visit the website for more information.''', style={'textAlign': 'center'}),
	#html.Div(dcc.Dropdown(options = [{'label': 'Line', 'value':'line'},{'label':'Bar','value':'bar'}])),
	html.Div([html.Div([
		dcc.Graph(
		id = 'violent_crime',
		figure = {'data':[violent_crime], 
			'layout':{'title':'Violent Crimes from 1999-2018', 
                'xaxis':{'title':'Year'},
                'yaxis':{'title':'Number of Crimes'
                        }
                       }
                   }
)],style = {'width': '48%', 'display': 'inline-block'}),
	html.Div([dcc.Graph(id = 'population_graph', 
		  figure = {'data':[population],
		   	 'layout':{'title':'Population in US from 1999-2018',
                'xaxis':{'title':'Year'},
                'yaxis':{'title':'U.S. Population'
                        }
                       }
                   }
)
],style = {'width': '48%', 'display': 'inline-block'})
]),
	   html.H4(children = 'Interactive Crime Comparison', style={'textAlign': 'center'}),
	   html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='Choose a feature or crime for the X-Axis'
            ), 
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='Choose a feature or crime for the Y-Axis'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
]),

	dcc.Graph(id = 'indicator-graphic'),
        html.H4(children = 'Crimes in terms of Population', style={'textAlign': 'center'}),
	    html.Div([

        html.Div([
            dcc.Dropdown(
                id='pop_yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='Choosen Feature or crime'
            ),
            dcc.RadioItems(
                id='pop_yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'display': 'inline-block'}),
]),
	dcc.Graph(id= 'population_df'),

	html.Div(children=[html.H4(children='Table of total Violent Crimes in America Since 1999 according to the FBI', style={'textAlign': 'center'})]),
    
	html.Div(children=[html.H6(children='Below is the data used in the visualizations, showing where missing values are located to explain certain results in the visualizations.  The original data is found at', style={'textAlign': 'center'}), html.A(children = 'FBI - Table 1', href='https://ucr.fbi.gov/crime-in-the-u.s/2018/crime-in-the-u.s.-2018/topic-pages/tables/table-1', target="_blank"),  generate_table(df)])
#cant get the link to be on the same level as the words or centered, so frustrating
])  

#Now add callback to make graph interactive
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
        return {
        'data': [dict(
            x=dff[dff['variable'] == xaxis_column_name]['value'],
            y=dff[dff['variable'] == yaxis_column_name]['value'],
            text=dff[dff['variable'] == yaxis_column_name]['Year'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'black'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 50, 'b': 90, 't': 10, 'r': 0},
            hovermode='closest',
            annotations = [dict(xref='paper',
                                        yref='paper',
                                        x=0.5, y=-0.25,
                                        showarrow=False,
                                        text ='This interactive figure allows you to chose both the X (left) and Y (right) axis data, pitting any crime or crime rate against another.  Hover over the data points for more information.  Additionally you can chose for the data to be in Linear or Logistic format.')]
        )
}
#Update Population graph
@app.callback(
    Output('population_df', 'figure'),
    [Input('pop_yaxis-column', 'value'),
     Input('pop_yaxis-type', 'value')])
def update_pop_graph(yaxis_column_name,yaxis_type):

    return {
        'data': [dict(
            x=dff['Population'],
            y=pop_df[pop_df['variable'] == yaxis_column_name]['value'],
            text=pop_df[pop_df['variable'] == yaxis_column_name]['Year'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': 'Population',
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 50, 'b': 90, 't': 10, 'r': 0},
            hovermode='closest',
            annotations = [dict(xref='paper',
                                        yref='paper',
                                        x=0.5, y=-0.25,
                                        showarrow=False,
                                        text ='This figure can show any crime or rate you choose against the U.S. Population, with the option to have the data appear in Linear or Logistic format.  Hover over the data points for more information.')]
        )
}

# have to make host = 0s 
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
