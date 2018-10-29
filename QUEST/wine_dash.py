import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)

wine_data = pd.read_csv('wine_data.csv')
clean_wine_data = wine_data.dropna(subset=["price","points","variety","country","region_1"]).copy(deep=True)

## Create list of countries for dropdown
countries_list = clean_wine_data['country'].unique()
countries_dict_list = []
for i in countries_list:
    countries_dict_list.append({'label':i,'value':i})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(
        children='Wine Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Label('Dropdown'),
    dcc.Dropdown(
        id = 'country',
        options=countries_dict_list,
        value=['US'],
        multi=True
    ),
    dcc.Dropdown(
        id = 'region_1',
        multi=True
    ),

    dcc.Graph(
        id='value-graph'
    )
])

## Change the region list based off the selected country
@app.callback(
    dash.dependencies.Output(component_id='region_1', component_property='options'),
    [dash.dependencies.Input(component_id='country', component_property='value')]
)
def refresh_regions(selected_country):
    filtered_countries = clean_wine_data[clean_wine_data['country'].isin(selected_country)] ## isin because it's checking series against list
    regions_list = filtered_countries['region_1'].unique()
    regions_dict_list = []
    for i in regions_list:
        regions_dict_list.append({'label':i,'value':i})

    return regions_dict_list

## Change list of wines based off country selected
@app.callback(
    ## component id is the id of the object you want to change
    ## component_property is the property of the object that you want to change
    dash.dependencies.Output(component_id='value-graph', component_property='figure'),
    ## Output will change based off what Input is
    [dash.dependencies.Input(component_id='country', component_property='value')]
)
def update_figure(selected_location):
    traces = []
    for i in range(len(selected_location)):
        filtered_df = clean_wine_data[clean_wine_data['country'] == selected_location[i]]
        agg_data = filtered_df.groupby('variety')['price','points'].mean()
        traces.append(go.Scatter(
            ## x-axis = price
            x= agg_data['price'],
            y= agg_data['points'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name= selected_location[i],
            text = agg_data.index.tolist()
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Average Price'},
            yaxis={'title': 'Average Quality'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

app.run_server(debug=True)
