import time
from pyspark.sql import SparkSession
from pyspark.sql import SparkSession, SQLContext

def create_spark_session(num_workers=2,
                         cores_per_worker=8,
                         cores_per_executor=8,
                         max_partition_bytes="128m",
                         shuffle_partitions=128):
    
    spark_session = SparkSession.builder \
    .master("spark://192.168.2.46:7077")\
    .appName(f"ScalabilityTest_{num_workers}")\
    .config("spark.dynamicAllocation.enabled", False)\
    .config("spark.dynamicAllocation.shuffleTracking.enabled",True)\
    .config("spark.shuffle.service.enabled", False)\
    .config("spark.dynamicAllocation.executorIdleTimeout","30s")\
    .config("spark.executor.cores", cores_per_executor)\
    .config("spark.executor.instances", num_workers) \
    .config("spark.cores.max", cores_per_worker*num_workers) \
    .config("spark.driver.port",9999)\
    .config("spark.blockManager.port",10005)\
    .config("spark.hadoop.fs.defaultFS", "hdfs://192.168.2.46:9000") \
    .config("spark.sql.files.maxPartitionBytes", max_partition_bytes)\
    .config("spark.sql.shuffle.partitions", shuffle_partitions)\
    .getOrCreate()

    return spark_session


def scalability_test(job,
                     num_workers, 
                     data_path="hdfs://192.168.2.46:9000/data/corpus-webis-tldr-17.json",
                     **spark_config):
    """
    Test scalability of job function

    Args:
    - job: The data processing function
    - job_parameters: The parameters to pass to the job function, should be in a lexi
    - num_workers: The number of workers to use
    - data_path: Path to reddit data in hdfs
    - spark_config: Additional configuration parameters for spark session

    Returns:
    - execution_time: Total execution time
    - data_load_time: Time for loading in data
    - processing_time: Data processing time
    """

    # create a spark session
    spark_session = create_spark_session(num_workers=num_workers, **spark_config)

    # create a spark context and SQL context
    spark_context = spark_session.sparkContext
    sqlContext = SQLContext(spark_context)

    start_time = time.perf_counter()

    # load the data
    df = sqlContext.read.json(data_path) #.sample(False, data_fraction)

    # time to load in data
    data_load_time = time.perf_counter() - start_time

    processing_start_time = time.perf_counter()

    # execute the job function
    result_df = job(df)[1]
    result_df.count()  # forces execution
    
    end_time = time.perf_counter()

    # time to perform data processing job
    processing_time = end_time - processing_start_time

    # total execution time
    execution_time = end_time - start_time
    
    print(f"Test with {num_workers} workers completed in {execution_time:.2f} sec")
    print(f"Time to load in data: {data_load_time:.2f} sec")
    print(f"Time to perform data processing task: {processing_time:.2f} sec")
    
    spark_session.stop()
    
    return execution_time, data_load_time, processing_time