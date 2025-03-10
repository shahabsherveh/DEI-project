import re
import pandas as pd
import csv
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

def preprocess_and_filter_bots(spark_context, reddit_json_path, botlist_csv_path):
    """
    Loads Reddit comments from HDFS, removes bot-generated comments, and preprocesses text.
    
    Args:
        spark_context (SparkSession): The Spark session.
        reddit_json_path (str): Path to the Reddit JSON data in HDFS.
        botlist_csv_path (str): Path to the bot list CSV file.
    
    Returns:
        DataFrame: A Spark DataFrame with cleaned and filtered data.
    """
    
    print(" Loading Reddit JSON data from HDFS...")
    df = spark_context.read.json(reddit_json_path)

    print(" Loading bot list from CSV...")
    bot_df = pd.read_csv(botlist_csv_path)
    bot_list = bot_df["AAbot"].dropna().unique().tolist()
    print(f" Loaded {len(bot_list)} bot names.")

    # Remove bot-generated comments
    df_filtered = df.filter(~col("author").isin(bot_list))

    # Function to clean text
    def preprocess_text(text):
        if not text or text.strip() == "":
            return ""  # Handle empty text
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = text.strip()  # Trim extra spaces
        return text

    # Register UDF for text preprocessing
    preprocess_udf = udf(preprocess_text, StringType())

    # Apply text preprocessing
    df_cleaned = df_filtered.withColumn("normalizedBody", preprocess_udf(col("normalizedBody")))

    print(" Preprocessing completed. Ready for sentiment analysis!")
    
    return df_cleaned