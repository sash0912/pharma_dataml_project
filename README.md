Pharmaceutical Drug Demand Forecasting in healthcare

I am going to develop a project on data science that uses machine learning to predict the availability of medications in the future. The reason why I decided to undertake this project is that the availability of medications is a highly important factor in healthcare. It is essential that pharmacies stock the necessary amount of medications, as a shortage of medications means that patients cannot be treated properly, while excess medications result in wastage because of their expiry dates.

So, my plan is that using historical sales of medications, I can forecast the demand for the upcoming periods. In this way, a pharmacy can organize inventory more effectively. In this project, I will be able to work with cleaning the data, developing features, training the machine learning models, as well as applying them.

2. Datasets I Plan to Use

I am planning to analyze multiple datasets that I have downloaded from Kaggle. The sites are:

PharmaDrugSales.csv

DrugSalesData.csv

sample_Pharmaceutical_Drug_Sales.csv,

salesdaily.csv

salesweekly.csv

salesmonthly.csv

saleshourly.csv

These are the databases that have the sales data for various medications at varying intervals of time. Due to the varied nature of the sources, the structure is variable, with varying columns. Among the initial things that I want to look for is the standardization of the essential columns, such as:

date

product/dr

quantity sold

price

region/store

After standardizing, I will merge them together into a single, complete dataset that is amenable to forecasting.

3. Planned Data Processing Procedures

Standardizing Column Names

Since different datasets have different column names, I am planning to write a logic that will identify these columns for a uniform naming convention such as:

date

product

qty

price

region

This will make it easy to merge the two data sets.

Changing All Data to be at a Monthly Level  

The data is provided on a hourly, daily, weekly, and monthly basis.
In order to simplify the forecasting process, I am going to use monthly totals for all the values.

Filling Missing Months

For a product/region that has some missing months, I intend to fill the missing months with zero values ensuring that there are consistent timelines for a particular product/region.

Feature Engineering

For enhancing the accuracy of my model, I would develop features which can identify the following trends:

Lag factors (1, 2, 3, 6, 12 months prior)

Moving averages and moving standard deviations

Month & Quarter Data

Price-related attributes

Features such as these will assist the machine learning model in learning short-run as well as long-run cycles.

4. ML Algorithms

Three ML models that I plan to implement are:

RIDGE regression -
Simple linear regression model that can assist in forming a baseline for comparison.

Random Forest Regressor-
An example of a tree-based model that is capable of modeling nonlinear behavior in the data.

XGBoost-
A strong gradient boosting model that typically works best for structured time-series forecasting tasks.

Now, to compare these models, I will use the following metrics:

MAE (Mean Absolute Error)

RMSE (Root Mean Squared Error)

MAPE (Mean Absolute Percentage Error)

After that, I will choose the best-performing model, which I will use as my final forecasting model.

5. Public vs. Private Models (My Understanding and Plan)

Public Models

This pertains to the machine learning algorithms which are publicly available in libraries such as:

scikit

XG Boost
Examples: Ridge Regression, Random Forest, XGBoost Regressor 

Private Model

Now, after I have trained these algorithms with my desired set of datasets, the trained model that I acquire is private because: It is customized with my data set It identifies patterns that are exclusive to pharma sales Its weights and parameters are not publicly available Later on, I’ll store these trained models in files with the suffix ‘.pkl’ within a folder named ‘models’. 

6. Interactive Forecasting App (Planned For deployment process)

I have plans to design a simple UI with the use of Streamlit. Via this application, a client will be able to: Choose a drug Choose a region Predict how many months are to be forecasted View predictions in table form Display predictions on a line chart After developing the model, I plan to use this model with that Streamlit application to make a real-time forecast.
 
This is my plan so far, to my understadings, changes will be made as I develop the project further.


