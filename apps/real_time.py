from dash import Dash, dcc, html, Input, Output
import dash
from app import app
import plotly.express as px
import pandas as pd
import dash_daq as daq
import serial
import time

def serve_layout():
    return html.Div([
    html.H1('Data Visualization of Sensors'),
    dcc.Dropdown(['Temperature', 'Relative Humidity', 'Ultrasonic', 'Infrared', 'Light'], 'Temperature', id='dropdown'),
    dcc.Graph(id="graph1"),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0)
])

app.layout = serve_layout

@app.callback(
    Output("graph1", "figure"), 
    Input("dropdown", "value"),
    Input("interval-component", "n_intervals"))
def update_line_chart(sensor, n):
    data = pd.read_csv('real_time.csv')
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
    elif sensor == 'Light':
        fig = px.line(data[['time','Light']], x="time", y="Light", title='Light Intensity')
        return fig
