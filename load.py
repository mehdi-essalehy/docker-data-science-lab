import json
import pandas as pd
import psycopg2

url = input("csv url: ")
config_path = input("db config: ")

config_file = open(config_path)
config = json.load(config_file)

db_host = config['db_host']
db_name = config['db_name']
db_user = config['db_user']
db_pass = config['db_pass']
table_name = config['table_name']

conn = psycopg2.connect(
	host=db_host,
	database=db_name,
	user=db_user,
	password=db_pass)

url = 'http://winterolympicsmedals.com/medals.csv'
data = pd.read_csv(url)

columns = list(data.columns)
sql_columns_list = [col.replace(' ', '_') + " VARCHAR(255)" for col in columns]
sql_columns_string = ",".join(sql_columns_list)

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
sql = "CREATE TABLE " + table_name + "("
sql += sql_columns_string + ")"
cursor.execute(sql)
conn.commit()

tmp_df = 'tmp.csv'
data.to_csv(tmp_df, header = True, index = False)
f = open(tmp_df, 'r')

cursor.copy_from(f, table_name, sep=",")
print("Data inserted using copy_from_datafile() successfully....")
conn.commit()

cursor.close()
conn.close()