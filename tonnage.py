import pandas as pd
import numpy as np




def select_id_thk(row, tonnage_df):
    nb = row["NB"]
    pressure = row["max_pressure"]
    # filter tonnage data for same NB
    candidates = tonnage_df[tonnage_df["NB"] == nb]

    # case 1: find rows where max_pressure is enough
    valid = candidates[candidates["max_pressure"] >= pressure]

    if not valid.empty:
        # take the first matching (lowest rating that still works)
        chosen = valid.iloc[0]
        return pd.Series([chosen["ID"], chosen["thk"], chosen["rating"]])
    else:
        # nothing found → return blanks
        return pd.Series([None, None, None])


def give_ton_output(tonnage_df, pipes_df):
    # tonnage_df = pd.read_excel("tonnage.xlsx")
    # pipes_df = pd.read_excel("second_process.xlsx")

    pipes_df["max_pressure"] = pipes_df[["available_residual_head_at_start","residual_head_at_end"]].max(axis = 1)

    merged = pipes_df.merge(tonnage_df[["ID", "thk","density kg/m3","NB"]], left_on="new_iop", right_on="ID", how="left")
    # apply to pipes_df
    merged[["ID_rating", "thk_rating", "rating"]] = merged.apply(select_id_thk, axis=1, tonnage_df=tonnage_df)



    rating_map = {"PN6": "HDPE","PN8": "HDPE","PN10":"HDPE","PN12":"HDPE","PN16":"HDPE","PN18":"HDPE","PN20":"HDPE","K7":"DI","K9":"DI","MS":"MS"}

    # Apply mapping (others remain same)
    merged["moc"] = merged["rating"].replace(rating_map)



    merged["tonnage"]= ((np.pi * (((merged["ID_rating"]/1000) + ((merged["thk_rating"]/1000)*2))**2 - ((merged["ID_rating"]/1000)**2)) / 4) * merged["length"] * merged["density kg/m3"]/1000)

    total_tonnage = merged["tonnage"].sum()

    print("total tonnage",total_tonnage)

    # Group by new column and sum
    moc_tonnage = merged.groupby("moc")["tonnage"].sum().reset_index()

    print(moc_tonnage)

    # merged.to_excel("ton_output.xlsx")
    return merged

