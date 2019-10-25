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
trip_updates_df = pd.DataFrame()

if __name__ == "__main__": 
    try:
        conn = pymysql.connect(host=rds_host, port=3306, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    sql_tu = "select * from trip_updates"
    trip_updates_df = pd.read_sql(sql_tu,conn)
    trip_updates_df.to_pickle('trip_updates.pkl')
    
    print(trip_updates_df.head())
    conn.close()
