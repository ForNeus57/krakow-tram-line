"""
DataSaver class for saving data to disk.
"""

from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path

import pandas as pd
import geopandas as gpd

from ktl.acquisition.data.package import Package
from ktl.acquisition.data.saver_info import SavingInfo


@dataclass(frozen=True)
class Saver:
    """
    Class that saves data to disk.
    """
    data: Package
    save_info: SavingInfo
    pickle_extension: ClassVar[str] = ".pkl"
    excel_extension: ClassVar[str] = ".xlsx"

    def create_save_directories(self) -> None:
        """
        Method that creates necessary paths so that it will be able to save data.
        """
        Path(self.save_info.save_path).mkdir(parents=True, exist_ok=True)

    def save(self, *args) -> None:
        """
        Method that accepts data objects and iterates over their object attributes.
        Then if it is a pandas dataframe or geopandas dataframe it saves all the files to pickle of specified path.
        """
        self.create_save_directories()

        for arg in args:
            for attribute, value in arg.__dict__.items():
                # Make match case for performance
                if isinstance(value, (pd.DataFrame, gpd.GeoDataFrame)):
                    value.to_pickle(self.save_info.save_path.joinpath(attribute + Saver.excel_extension))