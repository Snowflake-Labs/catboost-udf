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
