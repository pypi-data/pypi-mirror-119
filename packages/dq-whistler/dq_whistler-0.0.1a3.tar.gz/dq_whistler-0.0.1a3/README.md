
## Overview

Whistler is an open source data quality and profiling tool. Whistler enables profiling of your raw data irrespective of size i.e in MB's GB's or even TB's. 
This module brings the power of Apache Spark execution engine for all your profiling needs. 


## 🐣 Getting Started

### 1. Install Whistler
```commandline
pip install dq-whistler
```

### 2. Create a Spark dataframe for you data
```commandline
# Sample Data
Age,Description
1,"abc"
2,"abc1"
3,
4,"abc4"
10,"xyz"
12,"null"
17,"abc"
20,"abc3"
23,
```
```python
# You can read data from all the supported sources as per Apache Spark module
df = spark.read.option("header", "true").csv("<your path>")
```

### 3. Create a config in the form of python dict or read it from any json file
```python
config = [
   {
      "name": "Age",
      "datatype": "number",
      "constraints":[
         {
            "name": "gt_eq",
            "values": 5
         },
         {
            "name": "is_in",
            "values": [1, 23]
         }
         
      ]
   },
   {
      "name": "Description",
      "datatype": "string",
      "constraints":[
         {
            "name": "regex",
            "values": "([A-Za-z]+)"
         },
         {
            "name": "contains",
            "values": "abc"
         }
         
      ]
   }
]
```

### 4. Build an instance of Data Quality Analyzer and execute the checks
```python
from dq_whistler import DataQualityAnalyzer

output = DataQualityAnalyzer(df, config).analyze()

print(output)

```
```python
[
    {
        "col_name": "Age",
        "total_count": 9,
        "null_count": 0,
        "unique_count": 9,
        "topn_values": {
            "1": 1,
            "2": 1,
            "3": 1,
            "4": 1,
            "10": 1,
            "12": 1,
            "17": 1,
            "20": 1,
            "23": 1
        },
        "min": 1,
        "max": 23,
        "mean": 10.222222222222221,
        "stddev": 8.303279138054101,
        "quality_score": 0,
        "constraints": [
            {
                "name": "gt_eq",
                "values": 5,
                "constraint_status": "failed",
                "invalid_count": 4,
                "invalid_values": [
                    "1",
                    "2",
                    "3",
                    "4"
                ]
            },
            {
                "name": "is_in",
                "values": [
                    1,
                    23
                ],
                "constraint_status": "failed",
                "invalid_count": 7,
                "invalid_values": [
                    "2",
                    "3",
                    "4",
                    "10",
                    "12",
                    "17",
                    "20"
                ]
            }
        ]
    },
    {
        "col_name": "Description",
        "total_count": 9,
        "null_count": 2,
        "unique_count": 7,
        "topn_values": {
            "abc": 2,
            "abc1": 1,
            "xyz": 1,
            "abc4": 1,
            "abc3": 1
        },
        "quality_score": 0,
        "constraints": [
            {
                "name": "regex",
                "values": "([A-Za-z]+)",
                "constraint_status": "success",
                "invalid_count": 0,
                "invalid_values": []
            },
            {
                "name": "contains",
                "values": "abc",
                "constraint_status": "failed",
                "invalid_count": 2,
                "invalid_values": [
                    "xyz",
                    "null"
                ]
            }
        ]
    }
]
```

## 📦 Roadmap

The list below contains the functionality that contributors are planning to develop for this module


* **Visualization**
  * [ ] Visualization of profiling  output

  
## 🎓 Important Resources


## 👋 Contributing

## ✨ Contributors

