import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_csv("/Users/andreaongaro/Desktop/GitHub-Project/Personal/Dashboarding/Dashboarding_with_python/Dash_dash/Data/vgsales.csv")

df = df[df["Platform"] == "PS3"]

a = df.groupby("Year").sum()["Global_Sales"].div(df.groupby("Year").size())       
fruits = a.index.astype("str").tolist()
counts = a.tolist()
#p = figure(x_range=fruits, plot_height=350, title="Global sales per game grouped by"+group,
#                       toolbar_location=None,tools="")

fig = go.Figure(data=[
    go.Bar(x=fruits, y=counts),
    #go.Bar(name='B', x=fruts, y=[12, 18, 29])
])

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)