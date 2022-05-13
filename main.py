from producer import producer
from streamer import streamer
import os


os.system(
    'hadoop jar BigData-1.0-SNAPSHOT.jar com.BigDataProject.TennisScore input output')

producer()
streamer()
