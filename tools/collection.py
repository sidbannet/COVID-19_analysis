"""
Classes to manage data frames

@author: siddhartha.banerjee
"""

import pandas as pd
import datetime
import numpy as np
import os
import matplotlib.pyplot as plt


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
                #['India'],
                ['Korea', 'South Korea'],
                #['Singapore'],
                ['Italy'],
                #['UK', 'United Kingdom'],
                #['Germany'],
                ['Spain'],
                ['Other'],
            ],
            'State': [
                #['Alabama', 'AL'],
                #['Alaska', 'AK'],
                #['Arizona', 'AZ'],
                #['Arkansas', 'AR'],
                ['California', 'CA'],
                #['Colorado', 'CO'],
                #['Connecticut', 'CT'],
                #['Delaware', 'DE'],
                ['Florida', 'FL'],
                #['Georgia', 'GA'],
                #['Hawaii', 'HI'],
                #['Idaho', 'ID'],
                ['Illinois', 'IL'],
                #['Indiana', 'IN'],
                #['Iowa', 'IA'],
                #['Kansas', 'KS'],
                #['Kentucky', 'KY'],
                ['Louisiana', 'LA'],
                #['Maine', 'ME'],
                #['Maryland', 'MD'],
                ['Massachusetts', 'MA'],
                ['Michigan', 'MI'],
                #['Minnesota', 'MN'],
                #['Mississippi', 'MS'],
                #['Missouri', 'MO'],
                #['Montana', 'MT'],
                #['Nebraska', 'NE'],
                #['Nevada', 'NV'],
                #['New Hampshire', 'NH'],
                ['New Jersey', 'NJ'],
                #['New Mexico', 'NM'],
                ['New York', 'NY'],
                #['North Carolina', 'NC'],
                #['North Dakota', 'ND'],
                #['Ohio', 'OH'],
                #['Oklahoma', 'OK'],
                #['Oregon', 'OR'],
                #['Pennsylvania', 'PA'],
                #['Rhode Island', 'RI'],
                #['South Carolina', 'SC'],
                #['South Dakota', 'SD'],
                #['Tennessee', 'TN'],
                #['Texas', 'TX'],
                #['Utah', 'UT'],
                #['Vermont', 'VT'],
                #['Virginia', 'VA'],
                ['Washington', 'WA'],
                #['West Virginia', 'WV'],
                #['Wisconsin', 'WI'],
                #['Wyoming', 'WY'],
                ['Other', 'US'],
                ['Rest of the World', 'ROW'],
            ],
        }

        dates = []

        for y in [2020]:
            for m in [1]:
                for d in np.arange(start=22, stop=32, step=1):
                    dates.append(
                        datetime.datetime(
                            year=int(y), month=int(m), day=int(d),
                        )
                    )
            for m in [2]:
                for d in np.arange(start=1, stop=30, step=1):
                    dates.append(
                        datetime.datetime(
                            year=int(y), month=int(m), day=int(d),
                        )
                    )
            for m in [3]:
                for d in np.arange(start=1, stop=32, step=1):
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

        self.conf = df_template.copy()
        self.dead = df_template.copy()
        self.recov = df_template.copy()
        self.conf_us = df_template_us.copy()
        self.dead_us = df_template_us.copy()
        self.recov_us = df_template_us.copy()

        self._initialize_values_()

    def _initialize_values_(self) -> None:
        """Initialize the dataframe with zero initial cases."""

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
            df.columns = df.columns.str.replace('/', '_')
            # Find which country bucket the data belong to
            for inum, icon in enumerate(df.Country_Region):
                con_buc = [
                    icon in self.__reg__['Country'][i] for i in range(
                        self.__reg__['Country'].__len__()
                    )
                ]
                if sum(con_buc) == 0:
                    con_buc[-1] = True
                country_name = \
                    self.__reg__['Country'][
                        [i for i, val in enumerate(con_buc) if val][0]
                    ][0]
                try:
                    number_of_cases = int(df.Confirmed[inum]) \
                                      + self.conf.at[idx, country_name]
                    self.conf.at[idx, country_name] = number_of_cases
                except ValueError:
                    pass  # Do nothing
                try:
                    number_of_cases = int(df.Deaths[inum]) \
                                      + self.dead.at[idx, country_name]
                    self.dead.at[idx, country_name] = number_of_cases
                except ValueError:
                    pass  # Do nothing
                try:
                    number_of_cases = int(df.Recovered[inum]) \
                                      + self.recov.at[idx, country_name]
                    self.recov.at[idx, country_name] = number_of_cases
                except ValueError:
                    pass  # Do nothing
            # Find out which US state it is
            for inum, icon in enumerate(df.Country_Region):
                if icon not in self.__reg__['Country'][0]:
                    try:
                        self.conf_us.at[idx, 'ROW'] += \
                            int(df.Confirmed[inum])
                    except ValueError:
                        pass  # Do nothing
                    try:
                        self.dead_us.at[idx, 'ROW'] += \
                            int(df.Deaths[inum])
                    except ValueError:
                        pass  # Do nothing
                    try:
                        self.recov_us.at[idx, 'ROW'] += \
                            int(df.Recovered[inum])
                    except ValueError:
                        pass  # Do nothing
                else:  # This is filtered US case
                    try:
                        istate = df.Province_State[inum].split(sep=', ')[-1]
                    except ValueError:
                        istate = 'US'
                    state_buc = [
                        istate in self.__reg__['State'][i] for i in range(
                            self.__reg__['State'].__len__()
                        )
                    ]
                    if sum(state_buc) == 0:
                        state_buc[-2] = True
                    state_name = \
                        self.__reg__['State'][
                            [i for i, val in enumerate(state_buc) if val][0]
                        ][1]
                    try:
                        number_of_cases = int(df.Confirmed[inum]) \
                                          + self.conf_us.at[idx, state_name]
                        self.conf_us.at[idx, state_name] = number_of_cases
                    except ValueError:
                        pass  # Do nothing
                    try:
                        number_of_cases = int(df.Deaths[inum]) \
                                          + self.dead_us.at[idx, state_name]
                        self.dead_us.at[idx, state_name] = number_of_cases
                    except ValueError:
                        pass  # Do nothing
                    try:
                        number_of_cases = int(df.Recovered[inum]) \
                                          + self.recov_us.at[idx, state_name]
                        self.recov_us.at[idx, state_name] = number_of_cases
                    except ValueError:
                        pass  # Do nothing

    def plots(self) -> tuple:
        """Plot the COVID trends."""
        fig = plt.figure('COVID trends')
        ax = fig.subplots(nrows=2, ncols=1)
        self.__window__ = int(3)
        fig, ax = self.__plot__(fig, ax)
        [axes.grid(True) for axes in ax.flat]
        [axes.set_xscale('log') for axes in ax.flat]
        [axes.set_yscale('log') for axes in ax.flat]
        [axes.set_xlabel('Total number of cases') for axes in ax.flat]
        [axes.set_ylabel('Daily average growth') for axes in ax.flat]
        ax[0].set_title('Confirmed cases')
        fig.suptitle('COVID trends')
        return fig, ax

    def __plot__(
            self,
            *args,
    ) -> tuple:
        """Plot a single figure with figures."""
        try:
            fig, ax = args
        except ValueError:
            fig = plt.figure('COVID trends')
            ax = fig.subplots(nrows=2, ncols=1)
        idx = self.__dates__.__len__()
        # Give the plots
        try:
            window = self.__window__
        except ValueError:
            window = 3
        end_at = int(window - 1)
        for icon in self.conf.columns[1:]:
            data = self.conf[icon].values
            x = data[:idx]
            x_diff = np.diff(x, prepend=0)
            y = self.moving_average(values=x_diff, window=window)
            ax[0].plot(x[end_at:], y, label=icon)
        for istate in self.conf_us.columns[1:]:
            data = self.conf_us[istate].values
            x = data[:idx]
            x_diff = np.diff(x, prepend=0)
            y = self.moving_average(values=x_diff, window=window)
            ax[1].plot(x[end_at:], y, label=istate)
        return fig, ax

    @staticmethod
    def moving_average(
            values: np.ndarray = None,
            window: int = None,
    ) -> np.ndarray:
        """Moving average."""
        weights = np.repeat(1.0, window) / window
        return np.convolve(values, weights, 'valid')
