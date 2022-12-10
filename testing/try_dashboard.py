from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import dash_daq as daq
import serial
import time
from datetime import datetime as dt
import os
import pandas as pd
from google.cloud import bigquery
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'smartroom-db-976fcb1d1541.json'
client = bigquery.Client()

def refresh():
    sql_query = """
    CREATE OR REPLACE TABLE sensor_data.sensor_db_alter AS
    SELECT
    * EXCEPT (time),
    CAST(time AS DATETIME) AS time
    FROM
    sensor_data.sensor_db
    """
    query_job = client.query(sql_query)

def select_date(date):
    refresh()
    result = pd.DataFrame(columns=['time','Temperature','RH','Distance','Dectection','Light'])
    temp = pd.DataFrame()
    date_input = date
    sql_query = f"""
    SELECT * FROM smartroom-db.sensor_data.sensor_db_alter 
    WHERE date LIKE '{date_input}'
    """
    query_job = client.query(sql_query)
    for row in query_job.result():
        temp['time'] = [row[6]]
        temp['Temperature'] = [row[1]]
        temp['RH'] = [row[2]]
        temp['Distance'] = [row[3]]
        temp['Dectection'] = [row[4]]
        temp['Light'] = [row[5]]
        result = pd.concat([result, temp])
        result = result.sort_values(by='time',ascending=True)
    #result.to_csv('result.csv', index=False)
    print(result)
    return result

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Data Visualization of Sensors'),
    dcc.Dropdown(['Temperature', 'Relative Humidity', 'Ultrasonic', 'Infrared', 'Light'], 'Temperature', id='dropdown'),
    dcc.DatePickerSingle(
        id = 'my-date-picker-single', 
        #date = dt(2022,11,1),
        min_date_allowed = dt(2022,11,1)
    ),
    html.Button(id='my-button', n_clicks=0, children="Search Date"),
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
    Input("interval-component", "n_intervals"),
    State("my-date-picker-single", "date"),
    Input("my-button", 'n_clicks')
    #prevent_initial_call=True
    )
    
def update_line_chart(sensor, n, date, n_clicks):
    # data = pd.read_csv('sensors_data.csv')
    # print(type(date))
    # print(date)
    data = select_date(date)
    #print(len(data[['time','Temperature']]))
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

# @app.callback(
#     Output('boolean-switch-output', 'children'),
#     Input('my-boolean-switch', 'on'))
# def move_servo(status):
#     serialcomm = serial.Serial('/dev/cu.usbmodem14403', 9600)
#     serialcomm.timeout = 1
#     if status == True:
#         serialcomm.write(b'1')
#         time.sleep(0.01)
#         return f'The light is off!'
#     else:
#         serialcomm.write(b'0')
#         time.sleep(0.01)
#         return f''

app.run_server(debug=False, host="0.0.0.0", port=8080)