from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Data Visualization of Sensors'),
    dcc.Dropdown(['Temperature', 'Relative Humidity', 'Ultrasonic', 'Infrared'], 'Temperature', id='dropdown'),
    dcc.Graph(id="graph"),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0)
])

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"),
    Input("interval-component", "n_intervals"))
def update_line_chart(sensor, n):
    data = pd.read_csv('sensors_data.csv')
    if sensor == 'Temperature':
        fig = px.line(data[['time','Temperature']], x="time", y="Temperature", title='Room Temperature (°C)')
        return fig
    elif sensor == 'Relative Humidity':
        fig = px.line(data[['time','RH']], x="time", y="RH", title='Relative Humidity (%)')
        return fig
    elif sensor == 'Ultrasonic':
        fig = px.line(data[['time','Distance']], x="time", y="Distance", title='Object Range (cm)')
        return fig
    elif sensor == 'Infrared':
        fig = px.line(data[['time','Detection']], x="time", y="Detection", title='Yes/No (1/0)')
        return fig

app.run_server(debug=True)