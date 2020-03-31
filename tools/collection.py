"""
Classes to manage data frames

@author: siddhartha.banerjee
"""

import pandas as pd
import datetime
import numpy as np
import os


class DataClass:
    """Import, collect and present data of COVID cases."""

    def __init__(self):
        """Initialize the class."""

        df_template = pd.DataFrame(data=None)
        df_template['Date'] = []
        df_template_us = df_template.copy()

        region_index = {
            'Country': [
                ['US', 'United States', 'United States of America'],
                ['China', 'Mainland China', ],
                ['India'],
                ['Korea', 'South Korea'],
                ['Singapore'],
                ['Italy'],
                ['UK', 'United Kingdom'],
                ['Germany'],
                ['Spain'],
                ['Other'],
            ],
            'State': [
                ['Alabama', 'AL'],
                ['Alaska', 'AK'],
                ['Arizona', 'AZ'],
                ['Arkansas', 'AR'],
                ['California', 'CA'],
                ['Colorado', 'CO'],
                ['Connecticut', 'CT'],
                ['Delaware', 'DE'],
                ['Florida', 'FL'],
                ['Georgia', 'GA'],
                ['Hawaii', 'HI'],
                ['Idaho', 'ID'],
                ['Illinois', 'IL'],
                ['Indiana', 'IN'],
                ['Iowa', 'IA'],
                ['Kansas', 'KS'],
                ['Kentucky', 'KY'],
                ['Louisiana', 'LA'],
                ['Maine', 'ME'],
                ['Maryland', 'MD'],
                ['Massachusetts', 'MA'],
                ['Michigan', 'MI'],
                ['Minnesota', 'MN'],
                ['Mississippi', 'MS'],
                ['Missouri', 'MO'],
                ['Montana', 'MT'],
                ['Nebraska', 'NE'],
                ['Nevada', 'NV'],
                ['New Hampshire', 'NH'],
                ['New Jersey', 'NJ'],
                ['New Mexico', 'NM'],
                ['New York', 'NY'],
                ['North Carolina', 'NC'],
                ['North Dakota', 'ND'],
                ['Ohio', 'OH'],
                ['Oklahoma', 'OK'],
                ['Oregon', 'OR'],
                ['Pennsylvania', 'PA'],
                ['Rhode Island', 'RI'],
                ['South Carolina', 'SC'],
                ['South Dakota', 'SD'],
                ['Tennessee', 'TN'],
                ['Texas', 'TX'],
                ['Utah', 'UT'],
                ['Vermont', 'VT'],
                ['Virginia', 'VA'],
                ['Washington', 'WA'],
                ['West Virginia', 'WV'],
                ['Wisconsin', 'WI'],
                ['Wyoming', 'WY'],
                ['Other', 'US'],
                ['Rest of the World', 'ROW'],
            ],
        }

        dates = []

        for y in [2020]:
            for m in [1]:
                for d in np.linspace(start=22, stop=31):
                    dates.append(
                        datetime.datetime(
                            year=int(y), month=int(m), day=int(d),
                        )
                    )
            for m in [2]:
                for d in np.linspace(start=1, stop=29):
                    dates.append(
                        datetime.datetime(
                            year=int(y), month=int(m), day=int(d),
                        )
                    )
            for m in [3]:
                for d in np.linspace(start=1, stop=29):
                    dates.append(
                        datetime.datetime(
                            year=int(y), month=int(m), day=int(d),
                        )
                    )

        self.__reg__ = region_index
        self.__dates__ = dates

        self.__jhudataloc__ = r'JHU_repo' \
                              + os.sep + 'csse_covid_19_data' \
                              + os.sep + 'csse_covid_19_daily_reports' \
                              + os.sep

        # Initialize the data frame
        for inum, icon in enumerate(region_index['Country']):
            df_template[icon[0]] = []

        for inum, istate in enumerate(region_index['State']):
            df_template_us[istate[1]] = []

        df_template.Date = self.__dates__
        df_template_us.Date = self.__dates__
        df_template.set_index('Date')
        df_template_us.set_index('Date')

        self.conf = df_template
        self.dead = df_template
        self.recov = df_template
        self.conf_us = df_template_us
        self.dead_us = df_template_us
        self.recov_us = df_template_us

        self._initialize_values_()

    def _initialize_values_(self) -> None:
        """Initialize the dataframe with zero initial cases."""

        self.conf.fillna(0)
        self.conf_us.fillna(0)
        self.recov.fillna(0)
        self.recov_us.fillna(0)
        self.dead.fillna(0)
        self.dead_us.fillna(0)

        for country in self.__reg__['Country']:
            self.conf[country[0]] = np.zeros_like(
                self.conf.__getitem__(country[0]),
                int,
            )
            self.dead[country[0]] = np.zeros_like(
                self.dead.__getitem__(country[0]),
                int,
            )
            self.recov[country[0]] = np.zeros_like(
                self.recov.__getitem__(country[0]),
                int,
            )
        for state in self.__reg__['State']:
            self.conf_us[state[1]] = np.zeros_like(
                self.conf_us.__getitem__(state[1]),
                int,
            )
            self.dead_us[state[1]] = np.zeros_like(
                self.dead_us.__getitem__(state[1]),
                int,
            )
            self.recov_us[state[1]] = np.zeros_like(
                self.recov_us.__getitem__(state[1]),
                int,
            )

    def parse(self) -> None:
        """Parse data from the database."""

        # Get data from each csv files of daily updates
        for idx, dt in enumerate(self.__dates__):
            filename = datetime.datetime.strftime(dt, '%m-%d-%Y')
            filepath = self.__jhudataloc__ + filename + '.csv'
            df = pd.read_csv(
                filepath_or_buffer=filepath,
            )
            for inum, icon in enumerate(df._values[:, 1]):
                con_buc = [
                    icon in self.__reg__['Country'][i] for i in range(
                        self.__reg__['Country'].__len__()
                    )
                ]
                if sum(con_buc) == 0:
                    con_buc[-1] = True
                # The country index in the data frame
                contry_name = \
                    self.__reg__['Country'][
                        [i for i, val in enumerate(con_buc) if val][0]
                    ][0]
                try:
                    number_of_cases = int(df._values[inum, -3]) \
                                      + self.conf.get_value(
                        index=idx,
                        col=contry_name,
                    )
                    self.conf.set_value(
                        index=idx,
                        col=contry_name,
                        value=number_of_cases,
                    )
                except ValueError as ve:
                    pass  # Do nothing
                try:
                    number_of_cases = int(df._values[inum, -2]) \
                                      + self.dead.get_value(
                        index=idx,
                        col=contry_name,
                    )
                    self.dead.set_value(
                        index=idx,
                        col=contry_name,
                        value=number_of_cases,
                    )
                except ValueError as ve:
                    pass  # Do nothing
                try:
                    number_of_cases = int(df._values[inum, -1]) \
                                      + self.recov.get_value(
                        index=idx,
                        col=contry_name,
                    )
                    self.recov.set_value(
                        index=idx,
                        col=contry_name,
                        value=number_of_cases,
                    )
                except ValueError as ve:
                    pass  # Do nothing
