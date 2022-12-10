from dash import dcc, html
from dash.dependencies import Input, Output

from app import app


def serve_layout() -> html.Div:
    return html.Div([
        html.H1("Smart Room Dashboard", style={'font-size': 75, 'text-align': 'center', 'font-family': 'Arial Black'}),

        html.Div([
            dcc.Link('real time data', href='/apps/real_time.py'),
            html.Br(),
            dcc.Link('historical data', href='/apps/historical.py'),
            html.Br()
        ], style={'margin': 30, 'text-align': 'center', 'font-family': 'Arial'})

    ], style={'background-color': 'white'})


app.layout = serve_layout()