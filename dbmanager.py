import glob
import os
import pandas as pd
import psycopg2

TABLE_NAME = 'apartment_price'
COLUMNS_LIST = ['실거래가아이디', '시군구코드', '자치구명', '법정동코드', '법정동명', '신고년도', 
                        '대지권면적', '건물면적', '층정보', '물건금액', '건축년도', '건물명']

host = 'fanny.db.elephantsql.com'
user = "uwbijmex"
password = 'eia2qSD-PDVIsJUMrCkkc9sviWRza1Dz'
database = 'uwbijmex'

def create_connection() : 
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cur = connection.cursor()
    return cur, connection

if __name__ == '__main__' :
    cur, connection = create_connection()
    rawdata_path = os.getcwd() + '\\rawdata\\'

    cur.execute("DROP TABLE IF EXISTS apartment_price;")

    create_table = """
    create table if not exists apartment_price (
        실거래가아이디 varchar(25) primary key not null,
        시군구코드 float,
        자치구명 varchar(128),
        법정동코드 float,
        법정동명 varchar(128),
        신고년도 float,
        대지권면적 float,
        건물면적 float,
        층정보 float,
        물건금액 float,
        건축년도 float,
        건물명 varchar(128)
    );
    """
    cur.execute(create_table)

    for filename in os.listdir(rawdata_path) :
        df = pd.read_csv(rawdata_path + filename, encoding = 'euc-kr')        
    
        df = df[df.건물주용도 == '아파트']
        print(filename)
        print(df.columns)
        df = df[COLUMNS_LIST]
        
        df['법정동코드'] = df['법정동코드'] - (df['시군구코드'] * 100000)
        df = df.tail(1000)

        columns_list = ', '.join(df.columns)
        insert_inst = "insert into apartment_price(%s) values(%s)"%(columns_list, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s')

        cur.executemany(insert_inst, df.values)

    connection.commit()
    connection.close()

def getTableAll(table) :
    cur, connection = create_connection()
    query = f"select * from {table}"
    cur.execute(query)
    data = cur.fetchall()   
    connection.close()
    return data

def create_feature_importance(df) :
    cur, connection = create_connection()
    cur.execute("DROP TABLE IF EXISTS feature_importance;")

    create_table = """
    create table if not exists feature_importance (
        field_name varchar(25),
        permutation_importance float,
        feature_importnace float
    );
    """
    cur.execute(create_table)

    columns_list = ', '.join(df.columns)
    insert_inst = "insert into feature_importance(%s) values(%s)"%(columns_list, '%s,%s,%s')
    
    cur.executemany(insert_inst, df.values)
    connection.commit() 
    connection.close()

def find_name_by_code(codetype, value) :
    cur, connection = create_connection()

    if codetype == "시군구코드" : selecttype = "자치구명"
    else : selecttype = "법정동명"
    
    query = f'select {selecttype} from {TABLE_NAME} where {codetype} = {value} LIMIT 1'
    cur.execute(query)
    data = cur.fetchone()    
    connection.close()
    return(data[0])

def insert_user_prediction(data) : 
    
    create_table = """
    create table if not exists user_prediction (
        시군구코드 float,
        법정동코드 float, 
        신고년도 float,
        대지권면적 float,
        건물면적 float,
        층정보 float,
        건축년도 float,
        건물명 varchar(128),
        자치구명 varchar(128),
        법정동명 varchar(128),
        예상물건금액 float
    );
    """
    cur, connection = create_connection()
    cur.execute("DROP TABLE IF EXISTS user_prediction;")
    cur.execute(create_table)

    columns_list = ', '.join(data.columns)
    insert_inst = "insert into user_prediction(%s) values(%s)"%(columns_list, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s')

    cur.executemany(insert_inst, data.values)
    connection.commit()
    connection.close()



