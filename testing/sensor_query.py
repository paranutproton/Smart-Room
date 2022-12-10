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

def select_date():
    refresh()
    result = pd.DataFrame(columns=['time','Temperature','RH','Distance','Dectection','Light'])
    temp = pd.DataFrame()
    date_input = input("Enter date: ")
    print(type(date_input))
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
    
select_date()

