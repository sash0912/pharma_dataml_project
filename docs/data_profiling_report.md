# Data Profiling Report


## Dataset: kaggle_drug_sales_data.csv

❌ Error reading file: Error tokenizing data. C error: Expected 11 fields in line 9, saw 12



## Dataset: kaggle_pharma_drug_sales.csv

- Number of rows: 50532
- Number of columns: 14

### Columns & Data Types

- Time: object
- Year: object
- Month: object
- Date: object
- Hour: int64
- Day: object
- AceticAcidDerivatives: float64
- PropionicAcidDerivatives: float64
- SalicylicAcidDerivatives: float64
- PyrazolonesAndAnilides: float64
- AnxiolyticDrugs: float64
- HypnoticsSndSedativesDrugs: float64
- ObstructiveAirwayDrugs: float64
- Antihistamines: float64

### Missing Values

- Time: 0
- Year: 0
- Month: 0
- Date: 0
- Hour: 0
- Day: 0
- AceticAcidDerivatives: 0
- PropionicAcidDerivatives: 0
- SalicylicAcidDerivatives: 0
- PyrazolonesAndAnilides: 0
- AnxiolyticDrugs: 0
- HypnoticsSndSedativesDrugs: 0
- ObstructiveAirwayDrugs: 0
- Antihistamines: 0

### Sample Rows

| Time             |   Year |   Month |   Date |   Hour | Day      |   AceticAcidDerivatives |   PropionicAcidDerivatives |   SalicylicAcidDerivatives |   PyrazolonesAndAnilides |   AnxiolyticDrugs |   HypnoticsSndSedativesDrugs |   ObstructiveAirwayDrugs |   Antihistamines |
|:-----------------|-------:|--------:|-------:|-------:|:---------|------------------------:|---------------------------:|---------------------------:|-------------------------:|------------------:|-----------------------------:|-------------------------:|-----------------:|
| 01-02-2014 08:00 |   2014 |       2 |      1 |      8 | Thursday |                       0 |                       0.67 |                        0.4 |                        2 |                 0 |                            0 |                        0 |                1 |
| 01-02-2014 09:00 |   2014 |       2 |      1 |      9 | Thursday |                       0 |                       0    |                        1   |                        0 |                 2 |                            0 |                        0 |                0 |
| 01-02-2014 10:00 |   2014 |       2 |      1 |     10 | Thursday |                       0 |                       0    |                        0   |                        3 |                 2 |                            0 |                        0 |                0 |
| 01-02-2014 11:00 |   2014 |       2 |      1 |     11 | Thursday |                       0 |                       0    |                        0   |                        2 |                 1 |                            0 |                        0 |                0 |
| 01-02-2014 12:00 |   2014 |       2 |      1 |     12 | Thursday |                       0 |                       2    |                        0   |                        5 |                 2 |                            0 |                        0 |                0 |

## Dataset: kaggle_sales_daily.csv

- Number of rows: 2106
- Number of columns: 13

### Columns & Data Types

- datum: object
- M01AB: float64
- M01AE: float64
- N02BA: float64
- N02BE: float64
- N05B: float64
- N05C: float64
- R03: float64
- R06: float64
- Year: int64
- Month: int64
- Hour: int64
- Weekday Name: object

### Missing Values

- datum: 0
- M01AB: 0
- M01AE: 0
- N02BA: 0
- N02BE: 0
- N05B: 0
- N05C: 0
- R03: 0
- R06: 0
- Year: 0
- Month: 0
- Hour: 0
- Weekday Name: 0

### Sample Rows

| datum    |   M01AB |   M01AE |   N02BA |   N02BE |   N05B |   N05C |   R03 |   R06 |   Year |   Month |   Hour | Weekday Name   |
|:---------|--------:|--------:|--------:|--------:|-------:|-------:|------:|------:|-------:|--------:|-------:|:---------------|
| 1/2/2014 |       0 |    3.67 |     3.4 |   32.4  |      7 |      0 |     0 |     2 |   2014 |       1 |    248 | Thursday       |
| 1/3/2014 |       8 |    4    |     4.4 |   50.6  |     16 |      0 |    20 |     4 |   2014 |       1 |    276 | Friday         |
| 1/4/2014 |       2 |    1    |     6.5 |   61.85 |     10 |      0 |     9 |     1 |   2014 |       1 |    276 | Saturday       |
| 1/5/2014 |       4 |    3    |     7   |   41.1  |      8 |      0 |     3 |     0 |   2014 |       1 |    276 | Sunday         |
| 1/6/2014 |       5 |    1    |     4.5 |   21.7  |     16 |      2 |     6 |     2 |   2014 |       1 |    276 | Monday         |

## Dataset: kaggle_sales_hourly.csv

- Number of rows: 50532
- Number of columns: 13

### Columns & Data Types

- datum: object
- M01AB: float64
- M01AE: float64
- N02BA: float64
- N02BE: float64
- N05B: float64
- N05C: float64
- R03: float64
- R06: float64
- Year: int64
- Month: int64
- Hour: int64
- Weekday Name: object

### Missing Values

- datum: 0
- M01AB: 0
- M01AE: 0
- N02BA: 0
- N02BE: 0
- N05B: 0
- N05C: 0
- R03: 0
- R06: 0
- Year: 0
- Month: 0
- Hour: 0
- Weekday Name: 0

### Sample Rows

| datum          |   M01AB |   M01AE |   N02BA |   N02BE |   N05B |   N05C |   R03 |   R06 |   Year |   Month |   Hour | Weekday Name   |
|:---------------|--------:|--------:|--------:|--------:|-------:|-------:|------:|------:|-------:|--------:|-------:|:---------------|
| 1/2/2014 8:00  |       0 |    0.67 |     0.4 |       2 |      0 |      0 |     0 |     1 |   2014 |       1 |      8 | Thursday       |
| 1/2/2014 9:00  |       0 |    0    |     1   |       0 |      2 |      0 |     0 |     0 |   2014 |       1 |      9 | Thursday       |
| 1/2/2014 10:00 |       0 |    0    |     0   |       3 |      2 |      0 |     0 |     0 |   2014 |       1 |     10 | Thursday       |
| 1/2/2014 11:00 |       0 |    0    |     0   |       2 |      1 |      0 |     0 |     0 |   2014 |       1 |     11 | Thursday       |
| 1/2/2014 12:00 |       0 |    2    |     0   |       5 |      2 |      0 |     0 |     0 |   2014 |       1 |     12 | Thursday       |

## Dataset: kaggle_sales_monthly.csv

- Number of rows: 302
- Number of columns: 9

### Columns & Data Types

- datum: object
- M01AB: float64
- M01AE: float64
- N02BA: float64
- N02BE: float64
- N05B: float64
- N05C: float64
- R03: float64
- R06: float64

### Missing Values

- datum: 0
- M01AB: 0
- M01AE: 0
- N02BA: 0
- N02BE: 0
- N05B: 0
- N05C: 0
- R03: 0
- R06: 0

### Sample Rows

| datum     |   M01AB |   M01AE |   N02BA |   N02BE |   N05B |   N05C |   R03 |   R06 |
|:----------|--------:|--------:|--------:|--------:|-------:|-------:|------:|------:|
| 1/5/2014  |   14    |   11.67 |    21.3 |  185.95 |     41 |      0 |    32 |   7   |
| 1/12/2014 |   29.33 |   12.68 |    37.9 |  190.7  |     88 |      5 |    21 |   7.2 |
| 1/19/2014 |   30.67 |   26.34 |    45.9 |  218.4  |     80 |      8 |    29 |  12   |
| 1/26/2014 |   34    |   32.37 |    31.5 |  179.6  |     80 |      8 |    23 |  10   |
| 2/2/2014  |   31.02 |   23.35 |    20.7 |  159.88 |     84 |     12 |    29 |  12   |

## Dataset: kaggle_sales_weekly.csv

- Number of rows: 70
- Number of columns: 9

### Columns & Data Types

- datum: object
- M01AB: float64
- M01AE: float64
- N02BA: float64
- N02BE: float64
- N05B: float64
- N05C: float64
- R03: float64
- R06: float64

### Missing Values

- datum: 0
- M01AB: 0
- M01AE: 0
- N02BA: 0
- N02BE: 0
- N05B: 0
- N05C: 0
- R03: 0
- R06: 0

### Sample Rows

| datum      |   M01AB |   M01AE |   N02BA |    N02BE |   N05B |   N05C |   R03 |   R06 |
|:-----------|--------:|--------:|--------:|---------:|-------:|-------:|------:|------:|
| 2014-01-31 |  127.69 |  99.09  | 152.1   |  878.03  |    354 |     50 |   112 |  48.2 |
| 2014-02-28 |  133.32 | 126.05  | 177     | 1001.9   |    347 |     31 |   122 |  36.2 |
| 2014-03-31 |  137.44 |  92.95  | 147.655 |  779.275 |    232 |     20 |   112 |  85.4 |
| 2014-04-30 |  113.1  |  89.475 | 130.9   |  698.5   |    209 |     18 |    97 |  73.7 |
| 2014-05-31 |  101.79 | 119.933 | 132.1   |  628.78  |    270 |     23 |   107 | 123.7 |

## Dataset: kaggle_sample_pharma_sales.csv

- Number of rows: 1000
- Number of columns: 11

### Columns & Data Types

- Drug Name: object
- Manufacturer: object
- Dosage Form: object
- Strength: object
- Package Size: object
- Units Sold: int64
- Revenue: object
- Sale Date: object
- Region: object
- Sales Representative: object
- Customer Type: object

### Missing Values

- Drug Name: 0
- Manufacturer: 0
- Dosage Form: 0
- Strength: 0
- Package Size: 0
- Units Sold: 0
- Revenue: 0
- Sale Date: 0
- Region: 0
- Sales Representative: 0
- Customer Type: 0

### Sample Rows

| Drug Name   | Manufacturer   | Dosage Form   | Strength   | Package Size   |   Units Sold | Revenue   | Sale Date   | Region        | Sales Representative   | Customer Type   |
|:------------|:---------------|:--------------|:-----------|:---------------|-------------:|:----------|:------------|:--------------|:-----------------------|:----------------|
| Drug B      | Company W      | Tablet        | 100 mg/ml  | 50 g           |         1500 | $43833    | 2024-02-07  | South America | Susan Hernandez        | Clinics         |
| Drug B      | Company X      | Cream         | 500 mg     | 100 ml         |         1194 | $48717    | 2023-08-08  | South America | Jackie Wagner          | Clinics         |
| Drug E      | Company X      | Capsule       | 50 mg      | 60             |          618 | $8744     | 2024-06-15  | Africa        | Mariah Mccoy           | Hospitals       |
| Drug E      | Company X      | Injection     | 10 mg      | 100 ml         |         1455 | $25321    | 2024-07-15  | Asia          | Courtney Doyle         | Pharmacy        |
| Drug C      | Company V      | Tablet        | 100 mg/ml  | 50 g           |          130 | $13669    | 2023-08-13  | South America | Dawn Torres            | Clinics         |