
## Overview

Whistler is an open source data quality and profiling tool. Whistler enables profiling of your raw data irrespective of size i.e in MB's GB's or even TB's. 
This module brings the power of Apache Spark execution engine for all your profiling needs. 


## 🐣 Getting Started

### 1. Install Whistler
```commandline
pip install dq-whistler
```

### 2. Create a Spark dataframe for you data
```python
# You can read data from all the supported sources as per Apache Spark module
df = spark.read.option("header", "true").csv("<your path>")
```

### 3. Create a config in the form of python dict or read it from any json file
```python
config = [
   {
      "name": "Col1",
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
   },
   {
      "name": "Col2",
      "datatype": "number",
      "constraints":[
         {
            "name": "gt_eq",
            "values": 5
         },
         {
            "name": "is_in",
            "values": [1, 2]
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
        "col_name": "Col1",
        "total_count": 18720,
        "null_count": 0,
        "unique_count": 10,
        "topn_values": {
            "2016.03": 1872,
            "2010.03": 1872,
            "2012.03": 1872,
            "2015.03": 1872
        },
        "quality_score": 0,
        "constraints": [
            {
                "name": "regex",
                "values": "([A-Za-z]+)",
                "constraint_status": "failed",
                "invalid_count": 18720,
                "invalid_values": [
                    "2008.03",
                    "2009.03"
                ]
            },
            {
                "name": "contains",
                "values": "abc",
                "constraint_status": "failed",
                "invalid_count": 18720,
                "invalid_values": [
                    "2008.03",
                    "2009.03",
                    "2010.03"
                ]
            }
        ]
    },
    {
        "col_name": "Col2",
        "total_count": 18720,
        "null_count": 0,
        "unique_count": 5561,
        "topn_values": {
            "0": 6952,
            "1": 82,
            "2": 28,
            "3": 32,
            "5": 26,
            "16": 36,
        },
        "quality_score": 0,
        "constraints": [
            {
                "name": "gt_eq",
                "values": 5,
                "constraint_status": "failed",
                "invalid_count": 9553,
                "invalid_values": [
                    "-14407",
                    "-16171",
                    "-17160",
                    "-17061"
                ]
            },
            {
                "name": "is_in",
                "values": [
                    1,
                    2
                ],
                "constraint_status": "failed",
                "invalid_count": 18610,
                "invalid_values": [
                    "225544",
                    "243315",
                    "259381",
                    "262596"
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

