\# Standard Data Schema



\## Purpose

This document defines the canonical data schema used across the

entire Pharmaceutical Drug Demand Forecasting System.



All raw datasets will be transformed into this schema during the ETL phase.



---



\## Canonical Schema Definition



date        → datetime (ISO 8601)

product     → string (drug / category name)

qty         → float (units sold)

price       → float (optional, nullable)

region      → string (nullable)

source      → string (dataset origin)





\## Column Rules



\### date

\- Parsed from dataset-specific date/time columns

\- Converted to ISO 8601 format

\- Used as the time index for forecasting



\### product

\- Derived from drug category columns or drug name fields

\- One product per row (long format)



\### qty

\- Numeric quantity sold

\- Aggregated where required (hourly → daily → monthly)



\### price

\- Optional field

\- Extracted only when available

\- Otherwise stored as NULL



\### region

\- Optional

\- Populated only if dataset contains location information



\### source

\- Indicates origin dataset

\- Example values:

&nbsp; - kaggle\_sales\_hourly

&nbsp; - kaggle\_sales\_daily

&nbsp; - kaggle\_sales\_monthly



---



\## Dataset Mapping Decisions



\### Primary Datasets

\- kaggle\_sales\_hourly.csv

\- kaggle\_sales\_daily.csv

\- kaggle\_sales\_monthly.csv



\### Secondary Datasets

\- kaggle\_sales\_weekly.csv



\### Reference / Demo Dataset

\- kaggle\_sample\_pharma\_sales.csv



\### Excluded / Special Handling

\- kaggle\_drug\_sales\_data.csv (requires custom parsing logic)



---



\## Design Rationale

\- Long-format schema simplifies ML feature engineering

\- Flexible enough for multiple granularities

\- Compatible with time-series databases and APIs

\- Scales well as new datasets are added



