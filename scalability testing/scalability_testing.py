import time
from pyspark.sql import SparkSession
from pyspark.sql import SparkSession, SQLContext

def create_spark_session(num_workers):
    spark_session = SparkSession.builder \
    .master("spark://192.168.2.46:7077")\
    .appName("ScalabilityTest_"+str(num_workers))\
    .config("spark.dynamicAllocation.enabled", False)\
    .config("spark.dynamicAllocation.shuffleTracking.enabled",True)\
    .config("spark.shuffle.service.enabled", False)\
    .config("spark.dynamicAllocation.executorIdleTimeout","30s")\
    .config("spark.executor.cores", 8)\
    .config("spark.executor.instances", num_workers) \
    .config("spark.cores.max", 8*num_workers) \
    .config("spark.driver.port",9999)\
    .config("spark.blockManager.port",10005)\
    .config("spark.hadoop.fs.defaultFS", "hdfs://192.168.2.46:9000") \
    .getOrCreate()

    return spark_session


def horizontal_scalability_test(job, num_workers):
    """
    Test the horizontal scalability of job function

    Args:
    - job: The data processing function
    - num_workers: The number of workers to use

    Returns:
    - execution_time: The execution time of the job function
    """

    # stop the current session if exists
    try:
        spark_session.stop()
    except:
        pass

    # create a spark session
    spark_session = create_spark_session(num_workers)

    # create a spark context and SQL context
    spark_context = spark_session.sparkContext
    sqlContext = SQLContext(spark_context)

    start_time = time.perf_counter()

    # load the data
    df = sqlContext.read.json("hdfs://192.168.2.46:9000/data/corpus-webis-tldr-17.json") #.sample(False, data_fraction)
    df = df.select("subreddit", "content_len")

    # time to load in data
    data_load_time = time.perf_counter() - start_time

    
    processing_start_time = time.perf_counter()
    # execute the job function
    result_df = job(df)
    
    end_time = time.perf_counter()

    # time to to perform data processing job
    processing_time = end_time - processing_start_time
    

    # total execution time
    execution_time = end_time - start_time
    
    print(f"Test with {num_workers} workers completed in {execution_time:.2f} sec")
    print(f"Time to load in data: {data_load_time:.2f} sec")
    print(f"Time to perform data processing task: {processing_time:.3f} sec")
    
    spark_session.stop()
    
    return execution_time