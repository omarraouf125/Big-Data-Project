import os
import sys

bat_path = os.path.abspath("pyspark_python.bat")
os.makedirs(os.path.dirname(bat_path), exist_ok=True)

with open(bat_path, "w", encoding="utf-8") as f:
    f.write(f'@echo off\n"{sys.executable}" %*\n')

os.environ["PYSPARK_PYTHON"] = bat_path
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[1]")
    .appName("verify_pyspark_wrapper")
    .config("spark.python.worker.faulthandler.enabled", "true")
    .getOrCreate()
)

df = spark.createDataFrame([{"a": 1}])
df.show()
print("SUCCESS")
spark.stop()
