import serial
from datetime import datetime
import pandas as pd
import time

with serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1) as ser:
    counter=0
    while(True):
        data = pd.read_csv('co2_data.csv')
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        line = ser.readline()
        print(current_time, line.decode('UTF-8').strip().split())
        counter = counter+1
        if len(line.decode('UTF-8').strip().split())>3 and counter%30==0:
            temp = pd.DataFrame()
            temp['time'] = [current_time]
            temp['CO2'] = [line.decode('UTF-8').strip().split()[1]]
            temp['TVOC'] = [line.decode('UTF-8').strip().split()[4]]
            data = pd.concat([data, temp])
            data.to_csv('co2_data.csv', index=False)
            print('saved!')
    