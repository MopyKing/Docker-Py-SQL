import mysql
import mysql.connector
import requests
import time


# ########## DATABASE CREATION SECTION ##############
api_key="5b1ae42c-cc1b-496b-8c31-d05fd8b8092d"
# the next command will be responsible for connecting to a specific database
# since i am running this on our host maching, the host vaiable = localhost
# then im specifying the credentials for the database i created so as the name of the DB
db = mysql.connector.connect(
    host="db",
    user="root",
    passwd="1291996",
    database="testdatabase"
)
# next variable will be responsible on indexing and fetching data from the DB
my_cursor = db.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")  # creating a database with the name "testdatabase"

my_cursor.execute("Create table IF NOT EXISTS mycoins(Symbol varchar(100),Value int(100))")

# now im gonna insert values into 'coins' table i created - with the command executemany - to execute more than 1 cmd
# -----------------


# ####### FETCHING REST API DATA - FROM COINMARKETCAP ##############
# the URL i will use to fetch the data with REST API  :
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


# as noted in the API documentation of coinmarketcap , X-CMC... is responsible for my api-key input
# to request the desired data from the REST API.
# i use the Accept KEY to specify i want to recieve the response in JSON format
headers = {
    "X-CMC_PRO_API_KEY": api_key,
    'Accepts': 'application/json'
}

# the next dictionary will be responsible for specifying the desired data i need
# start 1 indicates that i want the coin ranked #1 which is BITCOIN ( UNTIL ETH 2.0 Avishay ;)? )
# limit will tell the API how many coins after the 1st i want, so lets set it to 1 since i only want BTC
# convert KEY will specify in which currency we want to display BTC value, lets go with USD
params = {
    "start": "1",
    "limit": "1",
    "convert": "USD"
}

btc_values = []
iteration_flag = 0
min = 0
max = 0
avg = 0
sum = 0
while(1):
    json = requests.get(URL, params=params, headers=headers).json()
    # the price we are looking for is located inside the json response under 'data' list, first dictionary, quote KEY
    # under USD, Price - with the help of online json parser
    btc_values.append(int(json['data'][0]['quote']['USD']['price']))
    sum += btc_values[-1]
    if iteration_flag == 0:
        print("Current BTC Value is : ", btc_values[-1], "$")
        min = max = btc_values[0]
    iteration_flag = 1

    if len(btc_values) >= 2:
        #print("Previous BTC Value is : ", btc_values[-2], "$")
        if btc_values[-1] > btc_values[-2]:
            print("if you hold BTC I suggest you sell it")
        else:
            print("if you don`t hold BTC already, I suggest you buy some... someday it will be worth +100k USD...",
                  " MARK MY WORDS !")
        if btc_values[-1] > max:
            max = btc_values[-1]
        if btc_values[-1] < min:
            min = btc_values[-1]
        avg = sum / len(btc_values)
        print("max BTC Value until now : ", max, "$")
        print("min BTC Value until now : ", min, "$")
        print("average BTC Value : %.2f" % avg, "$\n")

        # now im inserting data in to the DB table 'mycoins'
        sql = "INSERT INTO mycoins(Symbol, Value) VALUES (%s, %s)"
        val = ("BTC", btc_values[-1])
        my_cursor.execute(sql, val)
        db.commit()

        # lets display our newly row in the DB table 'mycoins'
        my_cursor.execute("Select * from mycoins")
        myresult = my_cursor.fetchall()
        for row in myresult:
            print(row)

    time.sleep(60)
