import serial
from datetime import datetime
import pandas as pd
import sys

with serial.Serial('/dev/cu.usbmodem141103', 9600, timeout=1) as ser:
    counter=0
    if sys.argv[1] == 'co2':
        while(True):
            data = pd.read_csv('co2_data.csv')
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            line = ser.readline()
            print(current_time, line.decode('UTF-8').strip())
            counter = counter+1
            if len(line.decode('UTF-8').strip().split())>3 and counter%30==0:
                temp = pd.DataFrame()
                temp['time'] = [current_time]
                temp['CO2'] = [line.decode('UTF-8').strip().split()[1]]
                temp['TVOC'] = [line.decode('UTF-8').strip().split()[4]]
                data = pd.concat([data, temp])
                data.to_csv('co2_data.csv', index=False)
                print('saved!')
    elif sys.argv[1] == 'ultrasonic':
        while(True):
            data = pd.read_csv('ultrasonic_data.csv')
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            line = ser.readline()
            print(current_time, "Distance: " + line.decode('UTF-8').strip())
            temp = pd.DataFrame()
            temp['time'] = [current_time]
            temp['Distance'] = [int(line.decode('UTF-8').strip())]
            if current_time == list(data['time'])[-1]:
                if list(data['Distance'])[-1] >= int(line.decode('UTF-8').strip()):
                    data = data[:-1]
            data = pd.concat([data, temp])
            data.to_csv('ultrasonic_data.csv', index=False)
    elif sys.argv[1] == 'dht11':
        while(True):
            data = pd.read_csv('dht11_data.csv')
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            line = ser.readline()
            if line.decode('UTF-8').strip() != '':
                print('{} Temperature: {} RH: {}'.format(current_time, line.decode('UTF-8').strip().split(", ")[0], line.decode('UTF-8').strip().split(", ")[1]))
                temp = pd.DataFrame()
                temp['time'] = [current_time]
                temp['Temperature'] = [float(line.decode('UTF-8').strip().split(", ")[0])]
                temp['RH'] = [float(line.decode('UTF-8').strip().split(", ")[1])]
                data = pd.concat([data, temp])
                data.to_csv('dht11_data.csv', index=False)
    