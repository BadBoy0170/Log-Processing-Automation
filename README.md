# Log Processing Automation & Anomaly Detection

This project simulates a log analysis pipeline, as described in my resume. It uses **PySpark** (to mimic **Azure Databricks**) to process raw Apache logs.

The script automates the analysis by:
1.  Parsing raw text logs into a structured format.
2.  Running a SQL query to identify **operational patterns** (e.g., status code counts).
3.  Running a second SQL query to detect **anomalies** (e.g., IPs generating the most errors), which simulates reducing manual review time.
4.  Exporting the results to CSV files for visualization in **Power BI**.

**Technologies:** Python, PySpark, SQL, Power BI

---

## ⚙️ How to Run the Project

### Step 1: Get the Data

This project requires a sample Apache log file.

To download a sample Apache log file, run the following command in your terminal:

```bash
curl -o sample_logs.log https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs
```

Place the `sample_logs.log` file in the same directory as the `process_logs.py` script.

### Step 2: Setup Environment Variables (Optional)

You can configure the log file name and the regex pattern using environment variables. If not set, default values will be used.

*   `LOG_FILE`: The name of the log file to process (default: `sample_logs.log`).
*   `LOG_REGEX`: The regular expression pattern to parse the log entries (default: `(\S+) (\S+) (\S+) \[(.*?)\] "(\S+ .*?)" (\d{3}) (\S+)`).

Example of setting environment variables:

```bash
export LOG_FILE="my_custom_logs.log"
export LOG_REGEX="your_custom_regex_pattern"
```

### Step 3: Set up Virtual Environment and Install Libraries

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyspark pandas
```

### Step 4: Run the Script

Run the script from your terminal:

```bash
python3 process_logs.py
```

This will run a local Spark job and create two new files:
*   `operational_patterns.csv`
*   `ip_anomalies.csv`

---

## 📊 Power BI Visualization Guide

Here is how to create the visualizations.

1.  Open Power BI Desktop.
2.  Click **"Get data"** -> **"Text/CSV"** and select `operational_patterns.csv`.
3.  Load the data.
4.  Repeat the process: Click **"Get data"** -> **"Text/CSV"** and select `ip_anomalies.csv`.
5.  Load the data. (You don't need to join them, just have them both available in the Fields pane).

### Visual 1: Operational Patterns (Pie Chart)

1.  Go to the "Report" view.
2.  Select the **Pie chart** visualization.
3.  From the `operational_patterns` table, drag `status_code` to the **Legend** field.
4.  Drag `count` to the **Values** field.
5.  You can customize the labels and title as needed.

### Visual 2: Anomaly Detection (Bar Chart)

1.  Create a new page in the report.
2.  Select the **Clustered bar chart** visualization.
3.  From the `ip_anomalies` table, drag `ip` to the **Axis** field.
4.  Drag `error_count` to the **Values** field.
5.  To show just the Top 10:
    *   Click on the `ip` field in the "Visualizations" pane, then select **"Filters"**.
    *   Under "Filter type", select **"Top N"**.
    *   Set "Show items" to **"Top"** and value to **10**.
    *   Drag `error_count` to the "By value" field.
    *   Click **"Apply filter"**.

### Visual 3: KPI Cards

1.  Create a new page in the report.
2.  Select the **Card** visualization.
3.  From the `operational_patterns` table, drag `count` to the **Fields** well.
4.  To display specific error counts (e.g., 404 errors):
    *   Drag `status_code` from `operational_patterns` to the **Filters on this visual** pane.
    *   Select **"404"** as the filter value.
5.  Rename the card title (e.g., "Total 404 Errors").
6.  Repeat this process for other status codes (e.g., "500" errors) on new Card visualizations.
7.  Finally, create a new **Dashboard** and arrange your visuals as desired.