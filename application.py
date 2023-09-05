# -*- coding: utf-8 -*-

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests


# Incorporate data
df = requests.get("https://fast-api-norges-bank-investment.onrender.com/v1/api/market_value/?by=country&currency=nok")

value_by_country = px.bar(df.json(), x='country', y='market_value', text_auto='.2s')
value_by_country.update_traces(textfont_size=12,
                               textangle=0,
                               textposition="outside",
                               cliponaxis=False)

share_by_country = px.pie(df.json(), values='market_value',
                          names='country',
                          title='Market Value',
                          hover_data=['market_value'],
                          labels={'market_value': 'Market Value'})
share_by_country.update_traces(textposition='inside', textinfo='percent+label')


# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
application = app.server


# page layout
index_page = html.Div([
    html.H1(children='Norges Bank Investment Management'),
    html.Br(),
    html.Div(children='This data has been taken from the following portal:'),
    dcc.Link('Norges Bank Investment Management', href='https://www.nbim.no/en/the-fund/investments/#/'),
    html.Div(children='''
        This is just a quick and simple demonstration of a use case that I imagined would help someone analyzing data 
        from portfolio of Norway's sovereign wealth fund, managed by Norges Bank Investment Managment.  
    '''),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(children='This chart can be selected using tools; option is visible when mouse pointer is hover on the chart. It can be downloaded as an image:'),
    html.H3('Market Value of Investments by Country, NOK'),
    dcc.Graph(
        id='market_value_nok',
        figure=value_by_country
    ),
    html.Br(),
    html.Div(children='This pie chart is interactive, if any of the country is deselected from the legends, it will recalculate the % share of remaining countries. Again, option to download the chart as an image'),
    html.H3('% Market Value by Country'),
    dcc.Graph(
        id='market_value_share',
        figure=share_by_country
    ),
])

app.layout = index_page

if __name__ == '__main__':
    application.run(debug=True, port=8080)
