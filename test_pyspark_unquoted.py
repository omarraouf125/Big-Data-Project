import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[1]').getOrCreate()
df = spark.createDataFrame([{'a': 1}])
df.show()
print("SUCCESS")
