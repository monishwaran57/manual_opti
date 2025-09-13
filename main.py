import pandas as pd
from dfs_sort import create_dfs_ordered_df
from optimizer import optimize_pipe_ids
from order_by_rhae import order_df_with_rhae_minimal_value
from reorder import find_rows_with_different_V_endpoints_in_df, create_order_list_to_arrange

MIN_VEL = 0.6
MAX_VEL = 3
MIN_PIPE_RHAE = 0
MIN_VILLAGE_RHAE = 28

input_df = pd.read_excel("sample.xlsx", sheet_name="Sheet1")

dfs_ordered_df = create_dfs_ordered_df(input_df)

rhae_minimal_ordered_df = order_df_with_rhae_minimal_value(ordered_df=dfs_ordered_df, min_vel=MIN_VEL, max_vel=MAX_VEL, iop_list=None)

processed_df = optimize_pipe_ids(ordered_df=rhae_minimal_ordered_df, min_vel=MIN_VEL, max_vel=MAX_VEL, min_pipe_rhae=MIN_PIPE_RHAE,
                  min_village_rhae=MIN_VILLAGE_RHAE, iop_list=None)

processed_df.to_excel("manul_count.xlsx")

dveidf = find_rows_with_different_V_endpoints_in_df(processed_df)

swapped_new_main_df_order_list = create_order_list_to_arrange(filtered_df=dveidf, main_df=processed_df)

main_df_with_new_order = processed_df.loc[swapped_new_main_df_order_list]

second_time_processed_df = optimize_pipe_ids(ordered_df=main_df_with_new_order, min_vel=MIN_VEL, max_vel=MAX_VEL, min_pipe_rhae=MIN_PIPE_RHAE,
                  min_village_rhae=MIN_VILLAGE_RHAE, iop_list=None)

second_time_processed_df.to_excel("second_process.xlsx")