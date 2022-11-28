from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas

US_FEDERAL_HOLIDAYS = {
    "1/1/2005", "1/17/2005", "1/20/2005", "2/21/2005", "5/30/2005", "7/4/2005",
    "9/5/2005", "10/10/2005", "11/11/2005", "11/24/2005", "12/25/2005", "12/26/2005",

    "1/1/2006", "1/2/2006", "1/16/2006", "2/20/2006", "5/29/2006", "7/4/2006",
    "9/4/2006", "10/9/2006", "11/10/2006", "11/11/2006", "11/23/2006", "12/25/2006"
                                                          
    "1/1/2007", "1/15/2007", "2/19/2007", "5/28/2007", "7/4/2007",
    "9/3/2007", "10/8/2007", "11/11/2007", "11/12/2007", "11/22/2007", "12/25/2007",

    "1/1/2008", "1/21/2008", "2/18/2008", "5/26/2008", "7/4/2008",
    "9/1/2008", "10/13/2008", "11/11/2008", "11/27/2008", "12/25/2008"
}


class PredictionDF:

    def __init__(self, csv_path: Path):
        self.df = pandas.read_csv(csv_path)

    def peak_hour_on_date(self, date: str):
        load_max = self.df.query(f"Date == '{date}'")["Load"].max()
        return self.df.query(f"Date == '{date}' & Load == {load_max}")["Hour"].values[0]


@dataclass
class Date:

    SEPERATOR = "/"

    datetime: datetime
    year: int
    month: int
    day: int

    def __init__(self, date_str: str):
        self.input_str = date_str
        self.month, self.day, self.year = map(int, date_str.split(self.SEPERATOR))
        self.datetime = datetime(self.year, self.month, self.day)
        self.is_holiday = date_str in US_FEDERAL_HOLIDAYS or self.weekday in {5, 6}

    @property
    def days_in_year(self) -> int:
        return self.datetime.timetuple().tm_yday

    @property
    def weekday(self) -> int:
        return self.datetime.weekday()
