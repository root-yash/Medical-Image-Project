import pandas as pd 
from pathlib import Path



def add_path_to_df(df: pd.DataFrame, data_dir: Path, type_: str, stage: str) -> pd.DataFrame:
    ending = ".tiff" if type_ == "image" else ".npy"
    
    dir_ = str(f"{data_dir}/{stage}_{type_}s") if type_ == "image" else f"{stage}_{type_}s"
    df[type_] = dir_ + "/" + df["id"].astype(str) + ending
    return df


def add_paths_to_df(df: pd.DataFrame, data_dir: Path, stage: str) -> pd.DataFrame:
    df = add_path_to_df(df, data_dir, "image", stage)
    df = add_path_to_df(df, data_dir, "mask", stage)
    return df


def prepare_data(data_dir: Path, stage: str, n_splits: int, random_seed: int) -> None:
    df = pd.read_csv(f"{data_dir}/{stage}.csv")
    df = add_paths_to_df(df, data_dir, stage)

    filename = f"{stage}_prepared.csv"
    df.to_csv(filename, index=False)


    return df