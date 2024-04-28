# Data Collection : การเก็บรวบรวมข้อมูลจจากแหล่งต่างๆ(DB & REST API)

# การอ่านข้อมูลจาก MySQL database
import os
import pymysql
import requests
import pandas as pd
import pymysql.cursors



# Config DB credential
class Config:
    MYSQL_HOST = "ใส่ข้อมูล host"
    MYSQL_PORT = 3306
    MYSQL_USER = "ใส่ข้อมูล user"
    MYSQL_PASSWORD = "ใส่ข้อมูล password"
    MYSQL_DB = "ใส่ข้อมูล db"
    MYSQL_CHARSET = "utf8mb4"

# Connect to DB

connection = pymysql.connect(host=Config.MYSQL_HOST,
                             port=Config.MYSQL_PORT,
                             user=Config.MYSQL_USER,
                             password=Config.MYSQL_PASSWORD,
                             db=Config.MYSQL_DB,
                             charset=Config.MYSQL_CHARSET,
                             cursorclass=pymysql.cursors.DictCursor)


# Query table audible_data
with connection.cursor() as cursor:
    # query ข้อมูลจาก table
    cursor.execute("SELECT * FROM audible_data;")
    result = cursor.fetchall()


# Query table audible_transaction
with connection.cursor() as cursor:
  cursor.execute("SELECT * FROM audible_transaction;")
  audible_transaction = cursor.fetchall()

# Convert to pandas
audible_data = pd.DataFrame(result)
audible_transaction = pd.DataFrame(audible_transaction)
# Set index
audible_data.set_index("Book_ID")

# Join table: audible_transaction & audible_data
transaction = audible_transaction.merge(audible_data, how="left" , left_on="Book_ID" , right_on="Book_ID")

# การอ่านข้อมูลจาก REST API

# Get data from REST API
url ="ลิ้งค์(ตัวแปร url)"
r = requests.get(url)
result_conversion_rate =r.json()

# Convert to Pandas
conversion_rate = pd.DataFrame(result_conversion_rate)

# Reset index to column "date"
conversion_rate = conversion_rate.reset_index().rename(columns={"index": "date"})

# convert column 'timestamp' to 'date' (transaction, conversion_rate)
transaction['date'] = transaction['timestamp']
transaction['date'] = pd.to_datetime(transaction['date']).dt.date
conversion_rate['date'] = pd.to_datetime(conversion_rate['date']).dt.date

# Join 2 dataframe (transaction, conversion_rate)
final_df = transaction.merge(conversion_rate, how="left", left_on="date", right_on="date")

# Remove "$" from column Price
final_df["Price"] = final_df.apply(lambda x: x["Price"].replace("$",""), axis=1)
# Convert type to float
final_df["Price"] = final_df["Price"].astype(float)

# Currency conversion(Price * conversion_rate)
def convert_rate(price,rate):
    return price * rate

final_df["THBPrice"] = convert_rate(final_df["Price"],final_df["conversion_rate"])

# Drop column "date"
final_df = final_df.drop("date" , axis=1)

# Save to CSV
final_df.to_csv("output.csv", index=False)