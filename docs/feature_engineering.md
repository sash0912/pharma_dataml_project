Feature Engineering – Time Series



Overview

This step generates machine-learning-ready features

from standardized pharmaceutical sales data.



\# Features Created

\- Monthly aggregated quantity sold

\- Lag features: 1, 3, 6, 12 months

\- Rolling mean: 3 and 6 months

\- Rolling standard deviation: 3 months



\# Purpose

\- Capture seasonality and trends

\- Enable supervised learning for forecasting

\- Improve model stability and accuracy



\# Output

\- data/features/sales\_features\_monthly.csv



\# Notes

\- Rows without sufficient history are removed

\- Features are product-specific



