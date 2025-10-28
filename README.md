# Log Processing Automation & Anomaly Detection

This project simulates a log analysis pipeline, as described in my resume. It uses **PySpark** (to mimic **Azure Databricks**) to process raw Apache logs.

The script automates the analysis by:
1.  Parsing raw text logs into a structured format.
2.  Running a SQL query to identify **operational patterns** (e.g., status code counts).
3.  Running a second SQL query to detect **anomalies** (e.g., IPs generating the most errors), which simulates reducing manual review time.
4.  Exporting the results to CSV files for visualization in **Tableau**.

**Technologies:** Python, PySpark, SQL, Tableau

---

## ⚙️ How to Run the Project

### Step 1: Get the Data

This project requires a sample Apache log file.

1.  Go to this link (a great source for sample log data): [https://www.kaggle.com/datasets/elikplim/apache-log](https://www.kaggle.com/datasets/elikplim/apache-log)
2.  Download the `apache_logs.txt` file.
3.  Rename the file to `sample_logs.log` and place it in the same directory as the `process_logs.py` script.

### Step 2: Install Libraries

You only need `pyspark` and `pandas`.
*(Note: `pyspark` requires a Java 8 or 11 environment to run. Most Macs have this, but if you get a Java error, you may need to install it.)*

```bash
pip3 install pyspark pandas
```

### Step 3: Run the Script

Run the script from your terminal:

```bash
python3 process_logs.py
```

This will run a local Spark job and create two new files:
* `operational_patterns.csv`
* `ip_anomalies.csv`

---

## 📊 Tableau Visualization Guide

Here is how to create the visualizations.

1.  Open Tableau. On the "Connect" pane, click **"Text File"** and select `operational_patterns.csv`.
2.  The data will load. At the top of the "Data Source" screen, click the **"Add"** button (next to Connections).
3.  Click **"Text File"** again and select `ip_anomalies.csv`.
4.  Tableau will load both files. (You don't need to join them, just have them both available in the Data pane).
5.  Click on a new worksheet.

### Visual 1: Operational Patterns (Pie Chart)

1.  In the "Data" pane, make sure `operational_patterns.csv` is selected.
2.  Change the Mark type from "Automatic" to **"Pie"**.
3.  Drag `Status Code` (from Dimensions) to the **Color** card.
4.  Drag `Count` (from Measures) to the **Angle** card.
5.  Drag `Count` and `Status Code` to the **Label** card to see the values.



### Visual 2: Anomaly Detection (Bar Chart)

1.  Create a new worksheet.
2.  In the "Data" pane, select the `ip_anomalies.csv` data source.
3.  Drag `Ip` (from Dimensions) to the **Rows** shelf.
4.  Drag `Error Count` (from Measures) to the **Columns** shelf.
5.  Click the sort icon on the X-axis to sort from highest to lowest.
6.  **To show just the Top 10:** Drag `Ip` (from Dimensions) onto the **Filters** card.
7.  In the filter box, go to the **"Top"** tab. Select **"By field"** and set it to: **Top 10 by Error Count (Sum)**.
8.  Click OK. This chart now shows the 10 most problematic IPs.



### Visual 3: KPI Cards

Tableau doesn't have a "Card" visual like Power BI, but you can make one easily.

1.  Create a new worksheet.
2.  Drag `Count` (from `operational_patterns.csv`) to the **Text** card.
3.  Drag `Status Code` to the **Filters** card.
4.  In the filter box, select **"404"** and click OK.
5.  The sheet will now just show a large number: the total count for 404 errors.
6.  Click the worksheet title and rename it "Total 404 Errors".
7.  Repeat this process on a new sheet for "500" errors.
8.  Finally, create a new **Dashboard** and drag all your new sheets onto it.