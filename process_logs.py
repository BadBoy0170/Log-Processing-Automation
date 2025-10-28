import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_extract

# --- Configuration ---
LOG_FILE = "sample_logs.log"
# This RegEx pattern captures the IP address (group 1) and the status code (group 8)
# Format: 1.2.3.4 - - [timestamp] "GET /request" STATUS_CODE ...
LOG_REGEX = r'(\S+) (\S+) (\S+) \[(.*?)\] "(\S+ .*?)" (\d{3}) (\S+)'
# ---

def process_logs():
    """
    Simulates a Databricks/Spark job to automate log analysis.
    - Parses raw logs
    - Identifies operational patterns
    - Detects anomalies (error-generating IPs)
    - Saves results to CSV for Power BI
    """
    
    print("Starting Spark session (simulating Databricks)...")
    
    # Initialize a local SparkSession
    spark = SparkSession.builder \
        .appName("LogAnalysis") \
        .master("local[*]") \
        .getOrCreate()
    
    # Set log level to WARN to reduce terminal noise
    spark.sparkContext.setLogLevel("WARN")

    # Check if data file exists
    if not os.path.exists(LOG_FILE):
        print(f"Error: Data file '{LOG_FILE}' not found.")
        print("Please download a sample Apache log file and name it 'sample_logs.log'.")
        spark.stop()
        return

    print(f"Loading data from '{LOG_FILE}'...")
    # 1. Data Loading: Load the raw log file as a text DataFrame
    df = spark.read.text(LOG_FILE)

    # 2. Log Parsing (Automation): Use regexp_extract to parse the log
    print("Parsing raw logs...")
    parsed_df = df.select(
        regexp_extract('value', LOG_REGEX, 1).alias('ip'),
        regexp_extract('value', LOG_REGEX, 6).alias('status_code')
    ).where(col('ip') != '') # Filter out any lines that didn't match

    # 3. SQL Analysis: Create a temporary view to run SQL queries
    parsed_df.createOrReplaceTempView("logs")

    # Query 1: Identify Operational Patterns (Count by status code)
    print("Running Query 1: Identifying operational patterns...")
    patterns_df = spark.sql("""
        SELECT status_code, COUNT(*) as count
        FROM logs
        GROUP BY status_code
        ORDER BY count DESC
    """)

    # Query 2: Detect Anomalies (IPs with high error rates)
    # This simulates "reducing manual review time" by isolating problem IPs
    print("Running Query 2: Detecting anomalies (top error IPs)...")
    anomalies_df = spark.sql("""
        SELECT ip, COUNT(*) as error_count
        FROM logs
        WHERE status_code >= 400 
        GROUP BY ip
        ORDER BY error_count DESC
    """)
    
    print("Queries complete. Saving results to CSV...")
    
    # 4. Output: Save results to CSV files
    # We convert to Pandas first to get a single, non-partitioned CSV file
    patterns_df.toPandas().to_csv("operational_patterns.csv", index=False)
    anomalies_df.toPandas().to_csv("ip_anomalies.csv", index=False)

    spark.stop()
    print("---")
    print("Log analysis complete. Output files created:")
    print("- operational_patterns.csv")
    print("- ip_anomalies.csv")
    print("You can now load these files into Power BI.")
    print("---")

if __name__ == "__main__":
    process_logs()