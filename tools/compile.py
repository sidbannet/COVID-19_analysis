"""
Classes to manage compiled output

@author: siddhartha.banerjee
"""

import os
import datetime
from tools.collection import DataClass


def update(
    dc: classmethod = DataClass,
    num_days_to_plot: int = 40,
) -> tuple:
    """Update the results."""
    assert(dc is DataClass), 'Incorrect class method'
    d = dc()
    compile_dir = r'compiled_data' + os.sep
    fig_name = 'COVID_trend_auto.png'
    now = datetime.datetime.now()
    try:
        d.parse()
        fig, ax = d.plots_timeseries()
        _ = [axes.set_ylim([10, 50000]) for axes in ax[:, 1].flat]
        _ = [axes.get_legend().remove() for axes in ax.flat]
        _ = ax[0, -1].legend(loc='upper right', title='Country')
        _ = ax[1, -1].legend(loc='upper right', title='US State')
        _ = ax[0, 0].set_xlim([0, num_days_to_plot])
        fig.suptitle(
            'COVID-19 trend' + '\n' + 'Last updated: '
            + now.strftime("%Y-%m-%d %H:%M:%S")
        )
        fig.set_size_inches(h=12, w=24)
        fig.savefig(fig_name)
        d.conf.to_csv(compile_dir + 'confirmed_cases.csv')
        d.dead.to_csv(compile_dir + 'death_cases.csv')
        d.recov.to_csv(compile_dir + 'recovered_cases.csv')
        d.conf_us.to_csv(compile_dir + 'confirmed_cases_US.csv')
        d.dead_us.to_csv(compile_dir + 'death_cases_US.csv')
        d.recov_us.to_csv(compile_dir + 'recovered_cases_US.csv')
        d.df_global.to_csv(compile_dir + 'compiled_data.csv')
        d.df_ndays.to_csv(compile_dir + 'days_to_10k.csv')
        d.df_ndays_us.to_csv(compile_dir + 'days_to_10k_US.csv')

        d._parse_timeseries_()
        d.to_csv(compile_dir + 'US_time_series_stat.csv')
    except AttributeError as ae:
        raise Exception('Incorrect class method used')
    return fig, ax
