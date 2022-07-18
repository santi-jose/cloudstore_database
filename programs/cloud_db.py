from scrape_makinex import products_df
from sql2py import create_server_connection
from sql2py import create_database
from sql2py import create_db_connection
from sql2py import execute_query
from sql2py import read_query
from sql2py import execute_list_query

#create the dataframe
df = products_df()

#establish connection to mySQL server
connection = create_server_connection("localhost", "root", "sqlV0idprogr@m")

#create database
create_database_query = "CREATE DATABASE cloudstore"
create_database(connection, create_database_query)

#connect to cloudstore database
connection = create_db_connection("localhost", "root", "sqlV0idprogr@m", "cloudstore")

#assign SQL query command to create tables
create_product_table = """
CREATE TABLE MAKINEX (
    product_name VARCHAR(50) NOT NULL,
    price VARCHAR(20),
    manufacturer VARCHAR(50),
    category VARCHAR(50),
    more_info VARCHAR(100) NOT NULL,
    img_link VARCHAR(100) NOT NULL
);
"""

execute_query(connection, create_product_table)

sql = """
    INSERT INTO MAKINEX (product_name, price, manufacturer, category, more_info, img_link)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

val = []

for index, row in df.iterrows():
    # print(row['Product Name'], row['Price'], row['More Info'])
    val.append([row['Product Name'], row['Price'], row['Manufacturer'], row['Category'], row['More Info'], row['Image Link']])
    # print(val[index])
    #execute_list_query(connection, sql, [row['Produt Name'], row['Price'], row['More Info']])
    # print('')

execute_list_query(connection, sql, val)