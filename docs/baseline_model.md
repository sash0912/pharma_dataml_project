Baseline Forecasting Model – Ridge Regression



Model Type

Ridge Regression (Linear model with L2 regularization)



Input Features

\- Lag features: 1, 3, 6, 12 months

\- Rolling means: 3 and 6 months

\- Rolling standard deviation: 3 months



Target Variable

\- Monthly quantity sold (`qty`)



Train/Test Strategy

\- Time-aware split

\- First 80% for training

\- Last 20% for testing



Evaluation Metrics

\- MAE (Mean Absolute Error)

\- RMSE (Root Mean Squared Error)



Purpose

\- Establish baseline performance

\- Benchmark for advanced models



