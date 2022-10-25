#!/usr/bin/env python3

# Imports
from snowflake.snowpark.session import Session
import snowflake.snowpark.functions as F
import snowflake.snowpark.types as T
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool

# Creating Snowpark Session
from config import snowflake_conn_prop
session = Session.builder.configs(snowflake_conn_prop).create()

# Generate training data
#

np.random.seed(42)

train_data = np.random.randint(0,
                               100,
                               size=(100, 5))

train_labels = np.random.randint(0,
                                 2,
                                 size=(100))

# create a dataframe
pdf = pd.DataFrame(train_data, columns=['I0','I1','I2','I3','I4'])
pdf['LABEL'] = train_labels.tolist()

# Train catboost classifier
model = CatBoostClassifier(iterations=2,
                           depth=2,
                           learning_rate=1,
                           loss_function='Logloss',
                           verbose=True)
model.fit(pdf.drop('LABEL', axis=1), pdf['LABEL'])
model.save_model("catboost_model_export.py", format="python")

# score the native model
pdf['NATIVE_MODEL'] = model.predict(pdf.drop('LABEL', axis=1)).tolist()

# score the python exported model
import catboost_model_export as cbm_export
model_preds_class = []
for ix, row in pdf.drop(['LABEL','NATIVE_MODEL'], axis=1).iterrows():
    model_preds_class.append(cbm_export.apply_catboost_model(row.values))
pdf['PYTHON_EXPORT_MODEL'] = model_preds_class

session.write_pandas(pdf, table_name='CATBOOST_TEST', auto_create_table=True, overwrite=True)

# score udf
@F.udf(session=session, name="cb_apply", stage_location="@CATBOOST", is_permanent=True,replace=True, imports=['catboost_model_export.py'])
def cb_apply(i1: float, i2: float, i3: float, i4: float, i5: float) -> float:
    import catboost_model_export as cbm_udf
    return cbm_udf.apply_catboost_model([i1,i2,i3,i4,i5])

session.table('CATBOOST_TEST').with_column('UDF_MODEL', cb_apply('I0','I1','I2','I3','I4')).show()
