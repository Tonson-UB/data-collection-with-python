# Demo Workshop Data Collection
This workshop collects data from MySQL database and REST API with python.

## Step to run (MySQL database)
1. Install PyMySQL
2. Create config database credential
3. Connect to MySQL database
4. Query data from table "audible_data" 
5. Query data from table "audible_transaction"
6. Convert data to pandas
7. Join table between "audible_transaction" and "audible_data"

## Step to run (REST API)
1. Get conversion rate data from REST API
2. Convert data to pandas
3. Reset index to column "date"
4. convert column 'timestamp' to 'date' 
5. Join 2 dataframe (transaction, conversion_rate)
6. Remove "$" from column Price
7. Currency conversion
8. Drop column "date"
9. Save output to CSV

## Setup
- Use PyMySQL to connect to a MySQL database.
```bash
# PyMySQL
! pip install pymysql
```
- Use Package requests to call REST API.
```bash
# requests
pip install requests
```