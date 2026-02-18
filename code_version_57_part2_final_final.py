import psycopg2
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import boto3

def e():
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()
    cur.execute("SELECT transction_id, status, type, amount FROM transactions")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data  # data is a list of tuples (values are ordered according to the order of the fields in the SELECT)

def t(data):
    data_f = [row for row in data if row[1] == 'success']
    data_g = {}
    for row in data_f:
        if row[2] not in data_g:
            data_g[row[2]] = 0
        data_g[row[2]] += 1
    rows = [(type, count) for type, count in data_g.items()]
    df = pd.DataFrame(rows, columns=['type', 'count'])
    df.to_parquet('output.parquet', compression='gzip')

def l():
    s3 = boto3.client('s3')
    f = open("output.parquet", "rb")
    s3.put_object(Bucket='my_bucket', Key='transformed.parquet', Body=f)
data = e()
t(data)
l()

