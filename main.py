import pandas as pd
from dfs_sort import create_dfs_ordered_df
from optimizer import optimize_pipe_ids


MIN_VEL = 0.6
MAX_VEL = 3
MIN_PIPE_RHAE = 0
MIN_VILLAGE_RHAE = 28

input_df = pd.read_excel("sample.xlsx", sheet_name="Sheet1")

dfs_ordered_df = create_dfs_ordered_df(input_df)

processed_df = optimize_pipe_ids(ordered_df=dfs_ordered_df, min_vel=MIN_VEL, max_vel=MAX_VEL, min_pipe_rhae=MIN_PIPE_RHAE,
                  min_village_rhae=MIN_VILLAGE_RHAE, iop_list=None)

processed_df.to_excel("manul_out.xlsx")
