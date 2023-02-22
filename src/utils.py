import pandas as pd
from typing import List, Tuple


def filter_df(df: pd.DataFrame, filter: str) -> pd.DataFrame:
    if filter == "All":
        return df
    elif filter == "Watchlist":
        return df[df["watchlist"] == True]
    else:
        tier_number = int(filter.replace("Tier ", ""))
        return df[df["tier"] == tier_number]
