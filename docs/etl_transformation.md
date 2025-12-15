ETL Transformation – Raw to Standard



\# Overview

This ETL step converts raw pharmaceutical sales datasets

into a single canonical schema used across the system.



\# Transformations Applied

\- Parsed dataset-specific date columns into ISO datetime

\- Identified drug category columns

\- Converted wide-format data into long-format

\- Added standard metadata columns

\- Removed invalid or null records



\# Output

\- data/processed/standardized\_sales.csv

\- Schema: date, product, qty, price, region, source





