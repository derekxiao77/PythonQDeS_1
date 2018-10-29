import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)

raw_data = pd.read_excel('Marketing Research Restaurant Data.xlsx')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
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
        id = 'dropdown',
        options=[
            {'label': 'Indian', 'value': 'Indian'},
            {'label': 'American', 'value': 'American'},
            {'label': 'French', 'value': 'French'},
            {'label': 'Mexican', 'value': 'Mexican'},
            {'label': 'Chinese', 'value': 'Chiense'},
            {'label': 'Italian', 'value': 'Italian'},
            {'label': 'Greek', 'value': 'Greek'}
        ],
        value=['Indian'],
        multi=True
    ),

    dcc.Graph(
        id='example-graph-2'
    )
])

@app.callback(
    dash.dependencies.Output(component_id='example-graph-2', component_property='figure'),
    [dash.dependencies.Input(component_id='dropdown', component_property='value')]
)
def update_figure(selected_location):
    traces = []
    for i in range(len(selected_location)):
        filtered_df = raw_data[raw_data['Q1 - Restaurant Type'] == selected_location[i]]
        traces.append(go.Scatter(
            x= filtered_df['Q2 - Location'].unique(),
            y= filtered_df.groupby('Q2 - Location')['Q6 - Annual Sales'].mean(),
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=selected_location[i],
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Restaurant Location'},
            yaxis={'title': 'Average Sales'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

app.run_server(debug=True)
