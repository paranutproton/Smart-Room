from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_daq as daq
import serial
import time

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Data Visualization of Sensors'),
    dcc.Dropdown(['Temperature', 'Relative Humidity', 'Ultrasonic', 'Infrared', 'Light'], 'Temperature', id='dropdown'),
    dcc.Graph(id="graph"),
    daq.BooleanSwitch(
    on=False,
    color="#9B51E0",
    label="Turn this on to turn off the light",
    id='my-boolean-switch'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0),
    html.Div(id='boolean-switch-output')
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
    elif sensor == 'Light':
        fig = px.line(data[['time','Light']], x="time", y="Light", title='Light Intensity')
        return fig

@app.callback(
    Output('boolean-switch-output', 'children'),
    Input('my-boolean-switch', 'on'))
def move_servo(status):
    serialcomm = serial.Serial('/dev/cu.usbmodem14403', 9600)
    serialcomm.timeout = 1
    if status == True:
        serialcomm.write(b'1')
        time.sleep(0.01)
        return f'The light is off!'
    else:
        serialcomm.write(b'0')
        time.sleep(0.01)
        return f''

app.run_server(debug=True)