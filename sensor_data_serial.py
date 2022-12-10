import serial
from datetime import datetime
import pandas as pd
import pandas_gbq
import sys
import time

def push_db():
    data = pd.read_csv('sensors_data.csv')
    data.to_gbq(destination_table='sensor_data.sensor_db',project_id='smartroom-db',if_exists='append')
    print('pushed')

with serial.Serial('/dev/cu.usbmodem1434403', 9600, timeout=1) as ser:
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
    elif sys.argv[1] == 'all':
        while(True):
            line = ser.readline()
            if line.decode('UTF-8').strip() != "":
                data = pd.read_csv('sensors_data.csv')
                now = datetime.now()
                my_dates = pd.date_range("now", periods=1)
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                current_date = now.strftime("%Y-%m-%d")
                counter = counter+1
                if counter%10==0: #30 the best
                    temp = pd.DataFrame()
                    temp['time'] = [current_time]
                    temp['date'] =  [current_date]
                    temp['Temperature'] = [float(line.decode('UTF-8').strip().split(", ")[0])]
                    temp['RH'] = [float(line.decode('UTF-8').strip().split(", ")[1])]
                    temp['Distance'] = [float(line.decode('UTF-8').strip().split(", ")[2])]
                    if line.decode('UTF-8').strip().split(", ")[3] == "Obstacle detected":
                        temp['Detection'] = [1]
                    elif line.decode('UTF-8').strip().split(", ")[3] == "No obstacle detected":
                        temp['Detection'] = [0]
                    temp['Light'] = [float(line.decode('UTF-8').strip().split(", ")[4])]
                    data = pd.concat([data, temp])
                    data.to_csv('sensors_data.csv', index=False)
                    data.to_csv('real_time.csv', index=False)
                    print('saved!')
                    print(type(now))
                    if len(data) > 300:
                        push_db()
                        data_temp = pd.read_csv('data_temp.csv')
                        data_temp.to_csv('sensors_data.csv', index=False)
                        print('done push')
                


    
    