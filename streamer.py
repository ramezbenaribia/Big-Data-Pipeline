from operator import delitem
import findspark
findspark.init()
from pyspark.sql import SparkSession
import random
from json import loads 
from kafka import KafkaConsumer
import os


def streamer():
    kafka_consumer = KafkaConsumer(
        'TennisTopic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='test',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for message in kafka_consumer:
        message = message.value
        print(message)
        f = open("tennis-after-kafka", "w")
        f.write(message["data"])
        f.close()
        break

    os.system("javac HBaseTennis.java")
    os.system("java HBaseTennis")

    spark = SparkSession.builder.getOrCreate()
    df = spark.read.load("output/part-r-00000", format="csv", sep="\t")
    df.sort("_c1", ascending=False).show()

    def CompareTwoPlayers(player1, player2):
        
        df.createOrReplaceTempView("TennisScore")
        df_player1 = spark.sql("SELECT * FROM TennisScore WHERE _c0=='" +  player1 + "' " )
        df_player2 = spark.sql("SELECT * FROM TennisScore WHERE _c0=='" +  player2 + "' " )


        score1 = df_player1.collect()[0]['_c1']
        score2 = df_player2.collect()[0]['_c1']

        print(player1 , "score is : " , score1 )
        print(player2 , "score is : " , score2 )

        if (score1 < score2):
            return(player2)
        elif (score1 > score2):
            return(player1)
        elif (score1 == score2):
            return(df2.collect()[int(random.uniform(0, 1))]['_c0'])

    player1 = input("Enter the first player name: ")
    player2 = input("Enter the second player name: ")

    print(CompareTwoPlayers(player1, player2))
