import pandas as pd
import pandas_gbq

while True:
    try:
        data = pd.read_csv('sensors_data.csv')
        if len(data) > 15:
            data.to_gbq(destination_table='sensor_data.sensor_db',project_id='smartroom-db',if_exists='append')
            print('pushed')
            data_temp = pd.read_csv('data_temp.csv')
            data_temp.to_csv('sensors_data.csv', index=False)
            print('done push')
    except:
        continue



