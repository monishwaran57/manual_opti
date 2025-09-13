from optimizer import give_parent_pipe_details


def create_order_list_to_arrange(filtered_df, main_df):

    main_df_index_list = main_df.index.to_list()

    # filtered_df["opti_count"] = filtered_df["opti_count"].str.replace(r"[\[\]']", "", regex=True)
    # filtered_df["opti_count"] = filtered_df["opti_count"].str.split(r",\s*")
    opti_count_parent_indices = {}
    for i, fdfseries in filtered_df.iterrows():
        opti_count = fdfseries['opti_count']
        opti_count.reverse()
        reversed_and_unique_opti_count = list(dict.fromkeys(opti_count))
        for v_endpoint in reversed_and_unique_opti_count:
            village_pipe_df = main_df[main_df['end_node'] == v_endpoint]
            row_index = village_pipe_df.index[0]
            village_pipe_dict = village_pipe_df.iloc[0].to_dict()
            village_pipe_dict["index"] = row_index

            parent_pipe = give_parent_pipe_details(child_start_node=village_pipe_dict['start_node'], ordered_df=main_df)

            parent_index_list = [int(village_pipe_dict['index']), parent_pipe['index']]
            while parent_pipe is not None:
                parent_pipe = give_parent_pipe_details(child_start_node=parent_pipe['start_node'], ordered_df=main_df)
                if parent_pipe is not None:
                    parent_index_list.append(parent_pipe['index'])
                else:
                    pass

            opti_count_parent_indices[v_endpoint] = parent_index_list
    print("what up!", opti_count_parent_indices)


    order_list = []
    seen = set()
    for endpoint, parent_index_list in opti_count_parent_indices.items():
        parent_index_list.sort()
        for i in parent_index_list:
            if i not in seen:
                order_list.append(i)
                seen.add(i)
    print("...order_list...\n", order_list)
    print(".....mainlsidkf.\n", main_df_index_list)

    new_main_df_order_list = order_list
    seen = set(order_list)
    for i in main_df_index_list:
        if i not in seen:
            new_main_df_order_list.append(i)
            seen.add(i)

    print("new main df order list:\n", new_main_df_order_list)
    return new_main_df_order_list


def find_rows_with_different_V_endpoints_in_df(df):
    # Step 1: Keep only rows that have "V" in opti_count
    df = df[df["opti_count"].str.contains("V", na=False)].copy()

    # Step 2: Convert to list
    df["opti_count"] = df["opti_count"].str.replace(r"[\[\]']", "", regex=True)
    df["opti_count"] = df["opti_count"].str.split(r",\s*")
    # Step 3: Filter rows with >=2 unique V endpoints
    def has_multiple_V_endpoints(lst):
        v_nodes = [item for item in lst if item.startswith("V")]
        return len(set(v_nodes)) > 1

    df = df[df["opti_count"].apply(has_multiple_V_endpoints)]

    # Save to Excel (optional)
    df.to_excel("ft1.xlsx", index=False)
    return df


# import pandas as pd
#
# manul_df = pd.read_excel("second_process.xlsx")
#
# dveidf = find_rows_with_different_V_endpoints_in_df(manul_df)
# # dveidf = pd.read_excel('ft1.xlsx')
#
# swapped_new_main_df_order_list = create_order_list_to_arrange(filtered_df=dveidf, main_df=manul_df)