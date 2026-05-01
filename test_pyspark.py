import os
import sys

bat_path = os.path.expanduser("~\\.pyspark_python.bat")
with open(bat_path, "w") as f:
    f.write(f'@echo off\n"{sys.executable}" %*\n')

os.environ['PYSPARK_PYTHON'] = bat_path
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[1]').getOrCreate()
df = spark.createDataFrame([{'a': 1}])
df.show()
print("SUCCESS")
