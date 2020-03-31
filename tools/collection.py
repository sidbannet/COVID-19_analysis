"""
Classes to manage data frames

@author: siddhartha.banerjee
"""

import pandas as pd
import datetime
import numpy as np
import os


class DataClass:
    """Import and collect data of COVID cases per country."""

    def __init__(self):
        """Initialize the class."""

        self.df = pd.DataFrame(data=None)
        region_index = {
            'Country': [
                ['US', 'United States', 'United States of America'],
                ['China', 'Mainland China', ],
                ['India'],
                ['Korea', 'South Korea'],
                ['Singapore'],
                ['Italy'],
                ['UK', 'United Kingdom'],
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
                ['Florida - FL'],
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
                ['Other - US', ],
                ['Other', ],
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
