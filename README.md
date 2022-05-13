
# Big Data Pipeline: 
# Prediction Of Tennis Matches Winner

This is a pipeline that uses many Big Data technologies to predict results of a tennis match.

## Requirements
Pull this image docker please. It is an Ubuntu image with **Hadoop** (2.7.2), **Spark** (2.2.1), **Kafka** (2.11-1.0.2) and **HBase** (1.4.8) 
```bash
   docker pull liliasfaxi/spark-hadoop:hv-2.7.2
``` 

## Data
- We took the date from Kaggle: **ATP  Matches**.
- The table consists of **900** lines.


## Architecture
![Architecture](https://user-images.githubusercontent.com/62619786/168388800-fbf15de1-cc8a-4fe3-98ad-c15d9763d567.PNG)

**-** Took the dataset from Kaggle which contains results from atp matches 2021 and done some preprocessing.

**-** Launched a mapReduce job to calculate the average sets scored by each player.

**-** Sent the generated output through Kafka to be stored in HBase.

**-** Launched Spark job to extract that data from HBase and to use it to predict the result of the winner  between two players mentioned in the users requests.


## Run Project
-Create 3 conatainers from image downloaded
**-** Create a network that will connect the three containers:
```bash
   docker network create --driver=bridge hadoop
``` 
**-** Create and launch the three containers:
```bash
   docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/spark-hadoop:hv-2.7.2
``` 
```bash
    docker run -itd -p 8040:8042 --net=hadoop --name hadoop-slave1 --hostname hadoop-slave1  liliasfaxi/spark-hadoop:hv-2.7.2
``` 
```bash
    docker run -itd -p 8041:8042 --net=hadoop --name hadoop-slave2 --hostname hadoop-slave2 liliasfaxi/spark-hadoop:hv-2.7.2
``` 
-Enter the master container to start using it and create  a directory
```bash
    docker exec -it hadoop-master bash
``` 
-Create  a directory that will contain our project
```bash
    mkdir BigDataPipline
``` 
-Now open  this project in a Terminal so that we can copy its content in our container
**-** To do that run those commands 
```bash
    docker cp .\Hadoop\target\BigData-1.0-SNAPSHOT.jar hadoop-master:/root/BigDataPipline
``` 
```bash
   docker cp .\HBaseTennis.java hadoop-master:/root/BigDataPipline
``` 
```bash
   docker cp .\main.py hadoop-master:/root/BigDataPipline 
``` 
```bash
   docker cp .\openTools.py hadoop-master:/root/BigDataPipline 
``` 
```bash
   docker cp .\producer.py hadoop-master:/root/BigDataPipline 
``` 
```bash
   docker cp .\streamer.py hadoop-master:/root/BigDataPipline 
``` 
```bash
   docker cp .\atp_matches_2021.txt hadoop-master:/root/BigDataPipline
``` 
-Now we have to go to the our directory to start runing the pipline and then make a copy of the file "atp_matches_2021.txt" in hadoop 
```bash
   hadoop fs –put atp_matches_2021.txt input
``` 
- After that we can start Hadoop ,Hbase and Kafka  
```bash
   python3 openTools.py
``` 
-Finaly open a new terminal in the hadoop-master container and run the "main.py" file  that contains the producer that will produce data to kafka and then will open the streamer that will consume that data and upload it in Hbase(don't forget to install the required packages for python)
```bash
   python3 main.py
``` 




