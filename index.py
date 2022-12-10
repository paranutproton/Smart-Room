from typing import Union

from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from apps import (
    home, real_time, historical
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        id='page-content',
        style={'margin-left': '2rem', 'margin-right': '2rem', 'padding': '1rem' '1rem'}
    )
], style={'background-color': '#F7F8FE'})


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname) -> Union[html.Div, str]:
    if pathname == '/':
        return home.serve_layout()
    elif pathname == '/apps/real_time.py':
        print('real_time')
        return real_time.serve_layout()
    elif pathname == '/apps/historical.py':
        print('historical')
        return historical.serve_layout()
    else:
        print(pathname)
        return '404'  # Page not found


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8803)