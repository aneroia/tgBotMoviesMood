##1##  pip install huggingface_hub
##2##  git clone https://huggingface.co/datasets/go_emotions
import pandas as pd
import numpy as np

df = pd.read_csv('go_emotions_dataset.csv')
print(df.head(5))
