"""
Simple Word Count Example
Counts word frequency in a text
"""
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("WordCount") \
    .master("local[*]") \
    .getOrCreate()

# Sample data
text_data = [
    "Apache Spark is amazing",
    "Spark is fast and powerful",
    "PySpark makes Spark easy to use",
    "Spark Spark Spark"
]

# Create RDD and perform word count
rdd = spark.sparkContext.parallelize(text_data)
word_counts = rdd.flatMap(lambda line: line.split()) \
    .map(lambda word: (word.lower(), 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda x: x[1], ascending=False)

print("\n=== Word Count Results ===")
for word, count in word_counts.collect():
    print(f"{word}: {count}")

spark.stop()
