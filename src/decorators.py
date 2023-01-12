import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from typing import Callable


def parallel(num_processes: int = 2) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """
    Decorator to parallelize non-vectorized operations on data frames.
    TODO: More detailed explanation.
    """
    def _parallel(
        func: Callable[[pd.DataFrame], pd.DataFrame]
        ) -> Callable[[pd.DataFrame], pd.DataFrame]:

        def wrapper(df: pd.DataFrame):
            index_splits = np.array_split(df.index.values, num_processes)
            results = Parallel(n_jobs=num_processes)(delayed(func)(df.loc[split]) for split in index_splits)
            return pd.concat(results)

        return wrapper
    return _parallel
