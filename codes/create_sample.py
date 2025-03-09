import pyspark as ps

conf = ps.SparkConf().setMaster('spark://192.168.2.46:7077').setAppName('splitData')\
.set('spark.cores.max',16)\
.set('spark.executor.cores', 4)


context = ps.SparkContext(conf=conf)

data = context.textFile('hdfs://192.168.2.46:9000/data/corpus-webis-tldr-17.json')


data_one_percent = data.sample(False, 0.01)

data_one_percent.saveAsTextFile('hdfs://192.168.2.46:9000/data/reddit_1percent.json')

context.stop()