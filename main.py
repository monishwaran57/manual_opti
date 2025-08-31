import pandas as pd
from dfs_sort import create_dfs_ordered_df

input_df = pd.read_excel("sample.xlsx", sheet_name="Sheet1")

dfs_ordered_df = create_dfs_ordered_df(input_df)
