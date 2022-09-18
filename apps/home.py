from dash import dcc, html
from dash.dependencies import Input, Output

from app import app


def serve_layout() -> html.Div:
    return html.Div([
        html.H1("Smart Room Dashboard", style={'font-size': 75, 'text-align': 'center', 'font-family': 'Arial Black'}),

        html.Div([
            dcc.Link('LED Status', href='/apps/led_status'),
            html.Br()
        ], style={'margin': 30, 'text-align': 'center', 'font-family': 'Arial'})

    ], style={'background-color': 'white'})


app.layout = serve_layout()