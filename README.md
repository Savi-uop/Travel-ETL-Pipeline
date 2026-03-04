# Associate Data Engineer Technical Challenge: Travel ETL Pipeline

## 📌 Project Overview
This repository contains a modular ETL (Extract, Transform, Load) pipeline designed for a Travel Booking domain. The application simulates a real-world scenario where raw, "dirty" data is processed through a structured pipeline to ensure data quality and integrity before being loaded into a PostgreSQL data warehouse for analytical reporting.

## 🛠️ Architecture & Tech Stack
* **Language:** Python 3.13.12
* **Data Processing:** Pandas (Cleaning, Validation, Transformation)
* **Database:** PostgreSQL (Storage & Optimization)
* **Cloud Integration:** Mock S3 Factory (Boto3 pattern)
* **Environment Management:** Python-dotenv

## 🏗️ The ETL Pipeline Logic
1.  **Extract:** Data is "uploaded" to a simulated S3 bucket (`mock_s3_bucket/`) and then "downloaded" to the landing zone. This demonstrates decoupling between the source and the processing engine.
2.  **Transform:**
    * **Deduplication:** Removes records with duplicate `booking_id`.
    * **Standardization:** Normalizes destination casing (Title Case) and parses inconsistent date formats into `YYYY-MM-DD`.
    * **Validation:** Identifies rows with null values or negative prices.
    * **Logging:** Invalid records are diverted to `rejected_records.log` instead of crashing the pipeline.
3.  **Load:** Clean data is upserted into the PostgreSQL `bookings` table.

## 🚀 Execution Instructions

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Savi-uop/Travel-ETL-Pipeline.git](https://github.com/Savi-uop/Travel-ETL-Pipeline.git)
    cd Travel-ETL-Pipeline
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment:**
    * Create a `.env` file from the provided `.env.example`.
    * Update your PostgreSQL credentials (DB_USER, DB_PASSWORD, etc.).

4.  **Run the Pipeline:**
    ```bash
    python generate_data.py  # Generates 10,000+ dirty records
    python run_pipeline.py    # Executes full ETL flow
    ```

## 📊 Database Design & Optimization
The PostgreSQL schema is designed for analytical performance. Key implementations include:
* **Primary Keys:** Enforced on `booking_id` to prevent data redundancy.
* **Check Constraints:** Enforced on `price` (>0) and `rating` (1-5).
* **Indexing Strategy:**
    * `idx_destination`: Speeds up geographical revenue reporting.
    * `idx_booking_date`: Optimized for monthly growth and trend analysis.

### Analytical Queries
The following queries are used for performance benchmarking:
1.  **Top 10 categories (Destinations) by revenue.**
2.  **Monthly growth analysis of booking volume.**
3.  **Average rating per country.**

## 📈 Scalability & Future Thinking
To scale this pipeline to **1 million+ records**, I would implement:
* **Distributed Computing:** Transition from Pandas to **Apache Spark (PySpark)** to process data in parallel across a cluster.
* **Orchestration:** Implement **Apache Airflow** to manage DAGs, schedule daily runs, and handle automated retries.
* **Table Partitioning:** Implement **Range Partitioning** on the `booking_date` column in PostgreSQL to maintain query performance as the table grows.
* **AWS Infrastructure:** Migrate from the Mock S3 Factory to a live **AWS S3** bucket with IAM roles restricted by the **Principle of Least Privilege**.
* Handling 1 Million+ Records: I would migrate the transformation layer from Pandas to Apache Spark (PySpark). Spark processes data across a cluster in parallel, whereas Pandas is limited by the memory of a single machine.

* Orchestration & Scheduling: Instead of manual execution, I would use Apache Airflow. This allows for automated scheduling (e.g., daily at 2 AM), dependency tracking between tasks, and automatic retries upon failure.

* Database Partitioning: I would implement Table Partitioning in PostgreSQL by booking_date. By creating monthly partitions, the database engine avoids full table scans, significantly improving query performance for time-series reports.

* Advanced Failure Handling: I would implement a Dead Letter Queue (DLQ) pattern. Any record failing validation would be diverted to a specific S3 "Errors" folder with a JSON metadata file explaining the failure reason, allowing for efficient auditing and re-processing.

## 🎥 Demonstration
A screen recording (10–15 minutes) is provided in the repository/submission link covering:
* Raw dataset inspection.
* ETL execution and log generation.
* PostgreSQL query output and optimization evidence (EXPLAIN ANALYZE).

## issue fixing

To ensure the pipeline is fully portable and environment-agnostic, I implemented a Service Mocking Pattern for the AWS S3 layer.
* **While the pipeline is designed to be fully compatible with the boto3 SDK, I utilized a custom Mock S3 Factory. 
* **This allows the ETL process to be executed without cloud costs, active AWS credentials, or external dependencies like Docker. 
* **This approach demonstrates Architecture Decoupling: the core ETL logic remains identical regardless of whether the storage backend is a local directory or a production S3 bucket.
* **This 'Local-First' development mindset ensures high developer productivity and robust unit testing capability."
