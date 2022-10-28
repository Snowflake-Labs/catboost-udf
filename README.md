# Snowflake Catboost UDF

[Catboost](https://catboost.ai/) is a high-performance open source library for gradient boosting on decision trees.

It supports [exporting models as Python code](https://catboost.ai/en/docs/concepts/python-reference_apply_catboost_model) with some important caveats:
  - Multiclassification models are not supported
  - The output returned is equivalent to 'RawFormulaVal' `prediction_type`

For `CatBoostClassifier` models, the `RawFormulaVal` will be negative for the `0` class and positive for the `1` class.
 
This repository contains example code for creating a `CatBoostClassifier` and using the exported Python to create a 
[Snowpark](https://www.snowflake.com/snowpark/) [User Defined Function](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udfs.html#creating-and-registering-a-named-udf).

## Setup

For Python and it's dependencies, we use [Anaconda](https://docs.conda.io/en/latest/miniconda.html) to setup an environment.

``` shell
conda env create -f environment.yml
```

Put your Snowflake connection settings into `config.py`, using the following template. The account property is a Snowflake [Account Locator](https://docs.snowflake.com/en/user-guide/admin-account-identifier.html). It's passed 

``` python
#!/usr/bin/env python3

snowflake_conn_prop = {
   "account": "ORG-account",
   "user": "USERNAME",
   "password": "PASSWORD"
   "role": "SYSADMIN",
   "database": "CATBOOST",
   "schema": "PUBLIC",
   "warehouse": "COMPUTE_WH",
}
```

Or via web browser authentication like so:

``` python
#!/usr/bin/env python3

snowflake_conn_prop = {
   "account": "ORG-account",
   "authenticator": "externalbrowser",
   "role": "SYSADMIN",
   "database": "CATBOOST",
   "schema": "PUBLIC",
   "warehouse": "COMPUTE_WH",
}
```

Run the following SQL in your Snowflake account to create a Database and a Stage for the user defined function.

``` sql
USE ROLE SYSADMIN;
CREATE DATABASE CATBOOST COMMENT = 'Database for CatBoost UDF, Stage and Test Data';
CREATE STAGE "CATBOOST"."PUBLIC".CATBOOST COMMENT = 'Stage for UDF objects';
```

# Usage

Create the model and UDF:
``` shell
conda activate catboost_snowpark
python cb.py
```

Verify in Snowflake:

``` sql
SELECT LABEL, NATIVE_MODEL, PYTHON_EXPORT_MODEL, CB_APPLY("I0","I1","I2","I3","I4") AS UDF_MODEL FROM CATBOOST_TEST;

SELECT NATIVE_MODEL, PYTHON_EXPORT_MODEL>0 FROM CATBOOST_TEST;
```

# Primary Maintainers

- Duncan Turnbull (@sfc-gh-dturnbull)

This is a community-developed package, not an official Snowflake offering. It comes with no support or warranty.
However, feel free to raise a github issue if you find a bug or would like a new feature

# License

Copyright 2022 Snowflake Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# Contributing

If you are interested in contributing to this project, [get started here](CONTRIBUTING.md)
