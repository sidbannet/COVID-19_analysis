"""
Classes to manage data frames

@author: siddhartha.banerjee
"""

import pandas as pd
import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
import tools.matplottools as mplttools


class DataClass:
    """Import, collect and present data of COVID cases."""

    def __init__(self):
        """Initialize the class."""

        df_template = pd.DataFrame(data=None)
        df_template['Date'] = []
        df_template_us = df_template.copy()
        df_global = pd.DataFrame(data=None)
        df_global['date'] = []
        df_global['country'] = []
        df_global['iso_alpha'] = []
        df_global['rate'] = []
        df_global['confirmed'] = []
        df_global['death'] = []
        df_global['recovered'] = []
        df_us = pd.DataFrame(data=None)
        df_us['date'] = []
        df_us['state'] = []
        df_us['iso_alpha'] = []
        df_us['rate'] = []
        df_us['confirmed'] = []
        df_us['death'] = []
        df_us['recovered'] = []

        region_index = {
            'Country': [
                ['US', 'United States', 'United States of America', 'USA'],
                ['China', 'Mainland China', 'CHN'],
                ['India', 'IND'],
                ['Japan', 'JPN'],
                ['Korea', 'South Korea', 'KOR'],
                ['Singapore', 'SGP'],
                ['Italy', 'ITA'],
                ['UK', 'United Kingdom', 'GBR'],
                ['Germany', 'DEU'],
                ['Spain', 'ESP'],
                ['Brazil', 'Brasil', 'BRA'],
                ['Australia', 'AUS'],
                ['Canada', 'CAN'],
                ['Argentina', 'ARG'],
                ['South Africa', 'South africa', 'ZAF'],
                ['Sweden', 'SWE'],
                ['Algeria', 'DZA'],
                ['Bangladesh', 'BGD'],
                ['Pakistan', 'PAK'],
                ['France', 'FRA'],
                ['Turkey', 'TUR'],
                ['Switzerland', 'CHE'],
                ['Belgium', 'BEL'],
                ['Netherlands', 'Holland', 'NLD'],
                ['Austria', 'AUT'],
                ['Portugal', 'PRT'],
                ['Norway', 'NOR'],
                ['Peru', 'PER'],
                ['Mexico', 'MEX'],
                ['Indonesia', 'IDN'],
                ['Israel', 'ISR'],
                ['Russia', 'Russian Federation', 'USSR', 'RUS'],
                ['Saudi Arabia', 'SAU'],
                ['Chile', 'CHL'],
                ['Malaysia', 'MYS'],
                ['Iran', 'Islamic Republic of Iran', 'IRN'],
                ['New Zealand', 'NZL'],
                ['World', 'Other', 'ROW'],
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

        self.__reg__ = region_index
        self.__jhudataloc__ = r'JHU_repo' \
                              + os.sep + 'csse_covid_19_data' \
                              + os.sep + 'csse_covid_19_daily_reports' \
                              + os.sep
        self.__jhudatalocts__ = r'JHU_repo' \
                                + os.sep + 'csse_covid_19_data' \
                                + os.sep + 'csse_covid_19_time_series' \
                                + os.sep
        dates = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.__jhudataloc__):
            for file in f:
                if '.csv' in file:
                    try:
                        dates.append(
                            datetime.datetime.strptime(
                                str.split(
                                    str.split(
                                        os.path.join(r, file),
                                        os.sep
                                    )[-1], '.csv'
                                )[0], '%m-%d-%Y'
                            )
                        )
                    except ValueError:
                        dates.append(
                            datetime.datetime.strptime(
                                str.split(
                                    str.split(
                                        os.path.join(r, file),
                                        os.sep
                                    )[-1], '.csv'
                                )[0], '%m-%d-%y'
                            )
                        )
        dates.sort()
        self.__dates__ = dates

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
        self.df_global = df_global
        self.df_us = df_us
        self.__filter_nconf_con__ = int(10000)
        self.__filter_nconf_state__ = int(5000)
        self.__n_outbreak__ = int(500)
        self.__window__ = int(3)

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
                    con_buc[-1] = True  # Catch all when not in the bucket
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
            # Aggregate the numbers on world-wide basis
            self.conf.at[idx, 'World'] = sum(self.conf.values[idx, 1:])
            self.dead.at[idx, 'World'] = sum(self.dead.values[idx, 1:])
            self.recov.at[idx, 'World'] = sum(self.recov.values[idx, 1:])
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
            for inum, country_id in enumerate(self.__reg__['Country'][:-1]):
                country_name = country_id[0]
                country_iso = country_id[-1]
                if idx < 3:
                    rate = float(1.0)
                else:
                    try:
                        rate = float(
                            (self.conf.at[idx, country_name] + 0.01) \
                            / (self.conf.at[idx - 3, country_name] + 0.01)
                        )
                    except ZeroDivisionError:
                        rate = float(1.0)
                self.df_global = pd.concat(
                    (
                        self.df_global,
                        pd.DataFrame(
                            [[
                                dt,
                                country_name,
                                country_iso,
                                float(max(rate, 1.0)),
                                int(self.conf.at[idx, country_name]),
                                int(self.dead.at[idx, country_name]),
                                int(self.recov.at[idx, country_name]),
                            ]],
                            columns=self.df_global.columns
                        ),
                    ),
                    ignore_index=True,
                )

    def _parse_timeseries_(self) -> None:
        """Parse and frame data from the time series data."""
        filepath_conf_US = self.__jhudatalocts__ \
                           + 'time_series_covid19_confirmed_US.csv'
        filepath_conf_g = self.__jhudatalocts__ \
                          + 'time_series_covid19_confirmed_global.csv'
        filepath_dead_US = self.__jhudatalocts__ \
                           + 'time_series_covid19_deaths_US.csv'
        filepath_dead_g = self.__jhudatalocts__ \
                          + 'time_series_covid19_deaths_global.csv'
        filepath_recv_g = self.__jhudatalocts__ \
                          + 'time_series_covid19_recovered_global.csv'
        df_conf_us = pd.read_csv(
            filepath_or_buffer=filepath_conf_US,
        )
        df_dead_us = pd.read_csv(
            filepath_or_buffer=filepath_dead_US,
        )
        df_conf_g = pd.read_csv(
            filepath_or_buffer=filepath_conf_g,
        )
        df_dead_g = pd.read_csv(
            filepath_or_buffer=filepath_dead_g,
        )
        df_recv_g = pd.read_csv(
            filepath_or_buffer=filepath_recv_g,
        )

        df_us_conf_UID = []
        df_us_conf_iso3 = []
        df_us_conf_State = []
        df_us_conf_Lat = []
        df_us_conf_Long = []
        df_us_conf_Key = []
        df_us_conf_Date = []
        df_us_conf_Confirmed = []
        df_us_conf_Rate = []
        df_us_dead_UID = []
        df_us_dead_Date = []
        df_us_dead_Population = []
        df_us_dead_Death = []

        date_col = int(11)
        daterange = df_conf_us.columns[date_col:]

        for irow in range(df_conf_us.shape[0]):
            if type(df_conf_us.UID.loc[irow]) is not np.int64:
                continue
            for iday, day in enumerate(daterange):
                df_us_conf_UID.append(int(df_conf_us.UID.loc[irow]))
                df_us_conf_iso3.append(df_conf_us.iso3.loc[irow])
                df_us_conf_State.append(df_conf_us.Province_State.loc[irow])
                df_us_conf_Lat.append(df_conf_us.Lat.loc[irow])
                df_us_conf_Long.append(df_conf_us.Long_.loc[irow])
                df_us_conf_Key.append(df_conf_us.Combined_Key.loc[irow])
                df_us_conf_Date.append(
                    datetime.datetime.strptime(day, '%m/%d/%y')
                )
                df_us_conf_Confirmed.append(
                    int(df_conf_us.loc[irow][iday + date_col])
                )
                if iday >= 2:
                    rate_of_growth = float(
                        df_conf_us.loc[irow][iday + date_col]
                        / (0.01 + df_conf_us.loc[irow][iday + date_col - 2])
                    )
                else:
                    rate_of_growth = float(
                        df_conf_us.loc[irow][iday + date_col]
                        / 0.01
                    )
                df_us_conf_Rate.append(rate_of_growth)
        rowdata_conf_us = {
            'UID': df_us_conf_UID,
            'iso3': df_us_conf_iso3,
            'State': df_us_conf_State,
            'Lat': df_us_conf_Lat,
            'Long': df_us_conf_Long,
            'Key': df_us_conf_Key,
            'Date': df_us_conf_Date,
            'Confirmed': df_us_conf_Confirmed,
            'Rate': df_us_conf_Rate,
        }

        for irow in range(df_dead_us.shape[0]):
            if type(df_dead_us.UID.loc[irow]) is not np.int64:
                continue
            for iday, day in enumerate(daterange):
                df_us_dead_UID.append(int(df_dead_us.UID.loc[irow]))
                df_us_dead_Date.append(
                    datetime.datetime.strptime(day, '%m/%d/%y')
                )
                df_us_dead_Population.append(
                    int(df_dead_us.Population.loc[irow])
                )
                df_us_dead_Death.append(
                    int(df_dead_us.loc[irow][iday + date_col +1])
                )
        rowdata_dead_us = {
            'UID': df_us_dead_UID,
            'Date': df_us_dead_Date,
            'Death': df_us_dead_Death,
            'Population': df_us_dead_Population,
        }

        self.df_geo_us = pd.merge(
            pd.DataFrame(rowdata_conf_us),
            pd.DataFrame(rowdata_dead_us),
            on=['UID', 'Date']
        ).sort_values(by='Date')
        self.df_geo_us['Number_Cases_per_1mil'] = (
            self.df_geo_us.Confirmed
            / (self.df_geo_us.Population + 0.0001)
        ) * 1e6
        self.df_geo_us['Mortality'] = 100 * (
            self.df_geo_us.Death
        ) / (
            self.df_geo_us.Confirmed + 0.0001
        )

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

    def plots_timeseries(
        self,
        n_outbreak: int = 500,
        n_filter_country: int = 10000,
        n_filter_state: int = 5000,
    ) -> tuple:
        """Plot the COVID trends in time series."""
        fig = plt.figure('COVID time series')
        ax = fig.subplots(nrows=2, ncols=3, sharex=True)
        self.__filter_nconf_con__ = n_filter_country
        self.__filter_nconf_state__ = n_filter_state
        self.__n_outbreak__ = n_outbreak
        fig, ax = self.__time_series_plot__(fig, ax)
        [axes.grid(True) for axes in ax.flat]
        [axes.set_xscale('log') for axes in ax.flat]
        [axes.set_xscale('linear') for axes in ax.flat]
        [axes.set_yscale('log') for axes in ax.flat]
        [axes.set_ylim([1000, 500000]) for axes in ax.flat]
        [axes.legend(title='Country') for axes in ax[0, :].flat]
        [axes.legend(title='US State') for axes in ax[1, :].flat]
        [axes.set_xlabel(
            'Days since ' + str(self.__n_outbreak__) + ' cases'
        ) for axes in ax[1, :].flat]
        ax[0, 0].set_title('Confirmed cases')
        ax[0, 1].set_title('Deaths')
        ax[0, 2].set_title('Recovered')
        fig.suptitle('COVID-19 time series trend')
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
        except AttributeError:
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

    def __time_series_plot__(self, *args) -> tuple:
        """Method to plots data in time series."""
        try:
            fig, ax = args
        except ValueError:
            fig = plt.figure('COVID-19 time series trends.')
            ax = fig.subplots(nrows=2, ncols=3, sharex=True)
        try:
            ncon_filter = self.__filter_nconf_con__
        except AttributeError:
            ncon_filter = 10000
        try:
            nstate_filter = self.__filter_nconf_state__
        except AttributeError:
            nstate_filter = 5000
        try:
            n_outbreak = self.__n_outbreak__
        except AttributeError:
            n_outbreak = 100
        # Number of days to report large number of cases from initial outbreak
        self.df_ndays = pd.DataFrame(data=None)
        self.df_ndays['Country'] = []
        self.df_ndays['Days'] = []
        self.df_ndays['Mortality'] = []
        self.df_ndays_us = pd.DataFrame(data=None)
        self.df_ndays_us['State'] = []
        self.df_ndays_us['Days'] = []
        self.df_ndays_us['Mortality'] = []

        for i, icon in enumerate(self.conf.columns[1:]):
            if self.conf[icon].values[-1] < int(ncon_filter):  # Filter data
                continue
            idx_since_100_count = np.where(
                np.asarray(self.conf[icon].values >= int(n_outbreak))
            )[0][0]
            days_to_10k_count = np.where(
                np.asarray(self.conf[icon].values
                           >= int(self.__filter_nconf_con__))
            )[0][0] - idx_since_100_count
            if icon is not 'World':
                ax[0, 0].plot(
                    self.conf[icon].values[idx_since_100_count:],
                    label=icon,
                    marker=mplttools.markers(i),
                    linewidth=3,
                )
                ax[0, 1].plot(
                    self.dead[icon].values[idx_since_100_count:],
                    label=icon,
                    marker=mplttools.markers(i),
                    linewidth=3,
                )
                ax[0, 2].plot(
                    self.recov[icon].values[idx_since_100_count:],
                    label=icon,
                    marker=mplttools.markers(i),
                    linewidth=3,
                )
                mortality = float(
                    self.dead[icon].values[-1]
                    / self.conf[icon].values[-1]
                ) * 100
                self.df_ndays = pd.concat(
                    (
                        self.df_ndays,
                        pd.DataFrame(
                            [[
                                str(icon),
                                int(days_to_10k_count),
                                float(mortality),
                            ]], columns=self.df_ndays.columns,
                        ),
                    ), ignore_index=True,
                )
            else:
                ax[0, 0].plot(
                    self.conf[icon].values[idx_since_100_count:],
                    label=icon,
                    linestyle='dashed', color='k', linewidth=1,
                )
                ax[0, 1].plot(
                    self.dead[icon].values[idx_since_100_count:],
                    label=icon,
                    linestyle='dashed', color='k', linewidth=1,
                )
                ax[0, 2].plot(
                    self.recov[icon].values[idx_since_100_count:],
                    label=icon,
                    linestyle='dashed', color='k', linewidth=1,
                )

        for i, istate in enumerate(self.conf_us.columns[1:]):
            if self.conf_us[istate].values[-1] < int(nstate_filter):  # Filter
                continue
            idx_since_100_count = np.where(
                np.asarray(self.conf_us[istate].values >= int(n_outbreak))
            )[0][0]
            days_to_10k_count = np.where(
                np.asarray(self.conf_us[istate].values
                           >= int(self.__filter_nconf_state__))
            )[0][0] - idx_since_100_count
            if istate is not 'ROW':
                ax[1, 0].plot(
                    self.conf_us[istate].values[idx_since_100_count:],
                    label=istate,
                    marker=mplttools.markers(i),
                    linewidth=2,
                )
                ax[1, 1].plot(
                    self.dead_us[istate].values[idx_since_100_count:],
                    label=istate,
                    marker=mplttools.markers(i),
                    linewidth=2,
                )
                ax[1, 2].plot(
                    self.recov_us[istate].values[idx_since_100_count:],
                    label=istate,
                    marker=mplttools.markers(i),
                    linewidth=2,
                )
                mortality = float(
                    self.dead_us[istate].values[-1]
                    / self.conf_us[istate].values[-1]
                ) * 100
                self.df_ndays_us = pd.concat(
                    (
                        self.df_ndays_us,
                        pd.DataFrame(
                            [[
                                str(istate),
                                int(days_to_10k_count),
                                float(mortality),
                            ]], columns=self.df_ndays_us.columns,
                        ),
                    ), ignore_index=True,
                )
            else:
                idx_since_100_count = np.where(
                    np.asarray(self.conf['US'].values >= int(n_outbreak))
                )[0][0]
                ax[1, 0].plot(
                    self.conf['US'].values[idx_since_100_count:],
                    label='USA',
                    linestyle='dashed', linewidth=1, color='k',
                )
                ax[1, 1].plot(
                    self.dead['US'].values[idx_since_100_count:],
                    label='USA',
                    linestyle='dashed', linewidth=1, color='k',
                )
                ax[1, 2].plot(
                    self.recov['US'].values[idx_since_100_count:],
                    label='USA',
                    linestyle='dashed', linewidth=1, color='k',
                )
        return fig, ax

    @staticmethod
    def moving_average(
            values: np.ndarray = None,
            window: int = None,
    ) -> np.ndarray:
        """Moving average."""
        weights = np.repeat(1.0, window) / window
        return np.convolve(values, weights, 'valid')
