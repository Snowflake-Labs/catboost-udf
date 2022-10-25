# catboost

## setup

Anaconda setup

``` shell
conda env create -f environment.yml
```

Snowflake connection settings into `config.py`

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

Snowflake account setup

``` sql
USE ROLE SYSADMIN;
CREATE DATABASE CATBOOST COMMENT = 'Database for CatBoost UDF, Stage and Test Data ';
CREATE STAGE "CATBOOST"."PUBLIC".CATBOOST COMMENT = 'Stage for UDF objects';
```

# usage

Create the model and UDF:
``` shell
conda activate catboost_snowpark
python cb.py
```

Verify in Snowflake

``` sql
SELECT LABEL, NATIVE_MODEL, PYTHON_EXPORT_MODEL, CB_APPLY("I0","I1","I2","I3","I4") AS UDF_MODEL FROM CATBOOST_TEST;

SELECT NATIVE_MODEL, PYTHON_EXPORT_MODEL>0 FROM CATBOOST_TEST;
```

# Primary Maintainers

- Duncan Turnbull (@sfc-gh-dturnbull)

This is a community-developed package, not an official Snowflake offering. It comes with no support or warranty.
However, feel free to raise a github issue if you find a bug or would like a new feature

# license

Copyright 2022 Duncan Turnbull

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
