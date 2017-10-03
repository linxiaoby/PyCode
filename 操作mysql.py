import pandas as pd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8")
# read
sql = "select * from tclass limit 3"
df = pd.read_sql(sql,conn,index_col="ClassID")
print df

# write
cur = conn.cursor()
cur.execute("drop table if exists tstudent")
cur.execute('create table user(id int,name varchar(20))' )
pd.io.sql.write_frame(df,"user",conn)