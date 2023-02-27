import pandas as pd


def filter_df(df: pd.DataFrame, filter: str) -> pd.DataFrame:
    """ Filter and return data frame according to the current radio item selection. """
    if filter == "All":
        return df
    elif filter == "Watchlist":
        return df[df["watchlist"] == 1]
    else:
        tier_number = int(filter.replace("Tier ", ""))
        return df[df["tier"] == tier_number]
