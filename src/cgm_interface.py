import requests
from datetime import datetime, timedelta
import pandas as pd
from .config import Config

class CGM_Reader:
    """Interface for CGM data acquisition"""

    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.authenticate()

    def authenticate(self):
        """This function sets up CGM API authentication"""
        # I will later impement Dexcom G7 authentication
        pass
    
    def get_current_bg(self):
        """This function gets most recent CGM reading
        
        Returns:
                tuple: (blood_glucose, timestamp)
        """

        # implement API call
        pass

    def get_bg_trends(self, minutes=30):
        """This function calculates blood glucose trends
        
        Returns:    
                dict: various trend calculations
        """
        readings = self.get_historical_readings(minutes)

        if len(readings) < 2:
            return {
                'trend_5min': 0,
                'trend_15min': 0,
                'trend_30min': 0
            }
        df = pd.DataFrame(readings)

        # Calculates rates of change (OMG OMG RATE OF CHANGE?!?!?! LIKE A DERIVATIVE?????)
        trends = {
             'trend_5min': self.calculate_trend(df, 5),
             'trend_15min': self.calculate_trend(df, 15),
             'trend_30min': self.calculate_trend(df, 30)
        }

        return trends
    
    def _calculate_trend(self, df, minutes):
        """This function hereby calculateth the rate of change over a specified timeframe"""
        recent_data = df[df['timestamp'] >=
                         datetime.now() - timedelta(minutes=minutes)]
        
        if len(recent_data) < 2:
            return 0
        
        time_diff = (recent_data['timestamp'].max() - 
                     recent_data['timestamp'].min()).total_seconds() / 60
        bg_diff = recent_data['blood_glucose'].iloc[-1] - \
                 recent_data['blood_glucose'].iloc[0]

        return bg_diff / time_diff if time_diff > 0 else 0
    