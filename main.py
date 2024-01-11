##1##  pip install huggingface_hub
##2##  git clone https://huggingface.co/datasets/go_emotions
import pandas as pd
import numpy as np
import pyarrow.parquet as pq

# Загрузка данных из файла Parquet
table = pq.read_table('go_emotions/simplified/validation-00000-of-00001.parquet')

# Преобразование данных в pandas DataFrame
df = table.to_pandas()

# Вывод первых нескольких строк данных
print(df.head())
print(len(df))
print("Column headers from list(df.columns.values):",
      list(df.columns.values))
