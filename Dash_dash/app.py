import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
#import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

#def generate_table(dataframe, max_rows=10):
#    return html.Table([
#        html.Thead(
#            html.Tr([html.Th(col) for col in dataframe.columns])
#        ),
#        html.Tbody([
#            html.Tr([
#                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#            ]) for i in range(min(len(dataframe), max_rows))
#        ])
#    ])


external_stylesheets = [dbc.themes.SLATE]

colors_general = {
    'background': '#556877'
}

style_top_bar = {'backgroundColor' : "#0066ff",
                    'textAlign': 'center',
                    "color": "white"
                    }

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.read_csv("../Data/vgsales.csv")

#dbc.Container(
body = dbc.Card(
        dbc.CardBody(
    [
        dbc.Row(
            dbc.Col(
                [   html.H1(children='Dashboarding with Dash')
                ],className="navbar navbar-expand-lg navbar-dark bg-primary"
            ),
        
        ),
         html.Br(),
        dbc.Row(
            [ 
                dbc.Col(
                    [dcc.Dropdown(
                        id='X_axis',
                        options=[{'label': i, 'value': i} for i in ["Year","Genre","Publisher"]],
                        value='Year'
                                ),html.Br(),
                    dcc.Dropdown(
                                id='Platform',
                                options=[{'label': i, 'value': i} for i in df["Platform"].unique().tolist()],
                                value='PS3'
                            )
                    ]),
                dbc.Col([
                    dcc.Graph(
                                id='first_graph',
                                config={
                        'displayModeBar': False
                    }
                            ),
                ]),
                dbc.Col([
                    dcc.Graph(
                        id='second_graph'
                            )
                ])
            ]
            )
    ]
    ), color = 'dark'
)


#fluid=True)
                
app.layout = html.Div([body])

@app.callback(
    Output('first_graph', 'figure'),
    Input('X_axis', 'value'),
    Input('Platform', 'value'))
def update_figure(X_selected,plat_selected):
    filtered_df = df[df["Platform"] == plat_selected]
    

    to_plot = filtered_df.groupby(X_selected).sum()["Global_Sales"].div(df.groupby(X_selected).size())       
    x = to_plot.index.astype("str").tolist()
    y = to_plot.tolist()
    

    fig = go.Figure(data=[
        go.Bar(x=x, y=y),
        
    ])

    fig.update_layout(
       template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    return fig

@app.callback(
    Output('second_graph', 'figure'),
    Input('X_axis', 'value'),
    Input('Platform', 'value'))
def update_figure_2(X_selected,plat_selected):
    filtered_df = df[df["Platform"] == plat_selected]
        
    temp = filtered_df.groupby(X_selected).sum()[["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]]
    temp = temp.div(temp.sum(axis=1),axis = 0)
    temp = temp.reset_index()
    temp[X_selected] = temp[X_selected].astype("str")
    

    X = temp[X_selected].tolist()
    GROUP = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]
    #Y = temp[]

    D = []
    for i in GROUP:
        D.append(go.Bar(name = i, x=X,y=temp[i].tolist()))

    fig = go.Figure(data=D)
    # Change the bar mode
    fig.update_layout(barmode='stack',
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)'
        )
     
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)