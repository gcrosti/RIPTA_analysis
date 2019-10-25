from rds_config import db_username, db_password, name_db
import pymysql
import sys
import logging
import pandas as pd

#rds settings
rds_host  = "mysqlforlambdatest.cftr8bracdbk.us-east-1.rds.amazonaws.com"
name = db_username
password = db_password
db_name = name_db

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, port=3306, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

sql_vp = "select * from vehicle_positions"
vehicle_positions_df = pd.read_sql(sql_vp,conn)
vehicle_positions_df.to_pickle('vehicle_positions.pkl')

conn.close()

print(vehicle_positions_df.head())