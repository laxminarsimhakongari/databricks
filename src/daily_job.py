"""Write one operational health record for the daily bundle job."""

import argparse
from datetime import datetime, timezone

from pyspark.sql import SparkSession


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = SparkSession.builder.getOrCreate()
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{args.catalog}`.`{args.schema}`")

    health_record = spark.createDataFrame(
        [
            {
                "job_name": "databricks-daily-job",
                "run_timestamp_utc": datetime.now(timezone.utc),
                "status": "SUCCESS",
            }
        ]
    )
    target_table = f"`{args.catalog}`.`{args.schema}`.job_health"
    health_record.write.mode("append").format("delta").saveAsTable(target_table)
    print(f"Wrote daily health record to {target_table}")


if __name__ == "__main__":
    main()