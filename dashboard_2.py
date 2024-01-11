# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests
import json


# Incorporate data
response = requests.get("https://fast-api-norges-bank-investment.onrender.com/v1/api/data/")
response = json.loads(response.text)
df = pd.read_json(eval(response['data']))

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# App layout
app.layout = html.Div([
    html.H1(children='Interactive Dashboard'),
    html.Hr(),
    html.Div(children='There are filters available on table, so it can be used to filter results for queries such as: "Companies with voting rights greater than 10" '),
    dash_table.DataTable(data=df.to_dict('records'),
                        columns=[
                              {"name": i, 'id': i} for i in df.columns
                           ],
                        filter_action='native',
                        style_table={
                            'height': 400,
                        },
                        style_data={
                            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        page_size=10),
    html.Hr(),
    html.Div(children='Following radio buttons can be used to update the chart below'),
    dcc.RadioItems(options=['country', 'region', 'incorporation_country'], value='market_value_nok',
                   id='controls-and-radio-item'),
    html.Br(),
    dcc.Graph(figure={}, id='controls-and-graph')
])


# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.bar(df, x=col_chosen, y='market_value_nok', text_auto='.2s')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
