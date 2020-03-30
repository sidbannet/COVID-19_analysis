"""
Classes to manage data frames

@author: siddhartha.banerjee
"""

import pandas as pd


class Country:
    """Import and collect data of COVID cases per country."""

    def __init__(self):
        """Initialize the class."""

        self.df = pd.DataFrame(data=None)
