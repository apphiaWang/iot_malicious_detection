import json
import psycopg2
from datetime import datetime,date

#request API content
REQUEST_CONTENT = {'uid', 'orig_h', 'orig_p', 'resp_h', 'resp_p', 'ts', 'orig_pkts', 'orig_ip_bytes', 'proto', 'service', 'label'}
#request return record time range
REQUEST_TIME_RANGE = 30

# get time offset for emulation data
today_date = date.today()
today_start_ts = datetime.strptime(str(today_date), "%Y-%m-%d").timestamp()
now_ts = datetime.timestamp(datetime.now())
OFFSET = now_ts-today_start_ts

def lambda_handler(event, context):
    conn = psycopg2.connect(dbname = 'dev',
                            host = '****',
                            port = '****',
                            user ='****',
                            password = '****'
                            )
    cur = conn.cursor()
    #get column head
    query = 'select pg_get_cols(\'emulate_data\');'
    cur.execute(query)
    col_head = (cur.fetchall())
    head_name = []
    for head_tuple in col_head:
        col = head_tuple[0]
        col = col.strip('(').strip(')')
        col = col.split(',')
        head_name.append(col[2])
    
    #get latest 30 second results
    #get current emulatedata's start ts
    query = "SELECT MIN(ts) FROM emulate_data"
    cur.execute(query)
    MIN_TS = cur.fetchall()
    MIN_TS = float(MIN_TS[0][0])
    
    #query updated data
    query = "SELECT * FROM emulate_data WHERE ts BETWEEN %s AND %s;"%(MIN_TS+OFFSET, MIN_TS+OFFSET+REQUEST_TIME_RANGE)
    cur.execute(query)
    query_results = cur.fetchall()
    
    #put together the records with header and leave only the requested content
    return_json = []
    for q in query_results:
        d = {}
        for index, field in enumerate(head_name):
            if(field in REQUEST_CONTENT):
                d[field] = q[index]
        return_json.append(d)
    
    #close the connector
    cur.close()
    conn.close()
    
    #return query results
    return {
        'statusCode': 200,
        'body': return_json
    }
