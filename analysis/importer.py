"""
Classes to manage data frames

@author: siddhartha.banerjee
"""

import pandas as pd


class DataClass:
    """Import and collect data of COVID cases per country."""

    def __init__(self):
        """Initialize the class."""

        self.df = pd.DataFrame(data=None)
        self.data = {
            'Country': [
                'US',
                'China',
                'India',
                ' Korea',
                'Singapore',
                'Italy',
                'UK',
                'Spain',
            ],
            'US State': [
                'Alabama - AL',
                'Alaska - AK',
                'Arizona - AZ',
                'Arkansas - AR',
                'California - CA',
                'Colorado - CO',
                'Connecticut - CT',
                'Delaware - DE',
                'Florida - FL',
                'Georgia - GA',
                'Hawaii - HI',
                'Idaho - ID',
                'Illinois - IL',
                'Indiana - IN',
                'Iowa - IA',
                'Kansas - KS',
                'Kentucky - KY',
                'Louisiana - LA',
                'Maine - ME',
                'Maryland - MD',
                'Massachusetts - MA',
                'Michigan - MI',
                'Minnesota - MN',
                'Mississippi - MS',
                'Missouri - MO',
                'Montana - MT',
                'Nebraska - NE',
                'Nevada - NV',
                'New Hampshire - NH',
                'New Jersey - NJ',
                'New Mexico - NM',
                'New York - NY',
                'North Carolina - NC',
                'North Dakota - ND',
                'Ohio - OH',
                'Oklahoma - OK',
                'Oregon - OR',
                'Pennsylvania - PA'
                'Rhode Island - RI',
                'South Carolina - SC',
                'South Dakota - SD',
                'Tennessee - TN',
                'Texas - TX',
                'Utah - UT',
                'Vermont - VT',
                'Virginia - VA',
                'Washington - WA',
                'West Virginia - WV',
                'Wisconsin - WI',
                'Wyoming - WY',
                'Other - US',
                'Other - Non US',
            ],
        }
