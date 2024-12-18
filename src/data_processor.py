import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from .config import Config


class DataProcessor:
    """Handles data preprocessing and feature engineering"""

    def __init__(self):
        self.config = Config()
        self.scalar = StandardScaler()

    def prepare_features(self, df):
        """This function creates feature set from raw data
        
        Arguments:
                    df: DataFrame with CGM and insulin data
        Returns:
                    DataFrame: Processed features
        """

        processed = df.copy()

        # Time based features
        processed['hour'] = pd.to_datetime(processed['timestamp']).dt.hour
        processed['day_of_week'] = pd.to_datetime(processed['timestamp']).dt.dayofweek

        # Create cyclical time features
        processed['hour_sin'] = np.sin(2 * np.pi * processed['hour']/24)
        processed['hour_cos'] = np.cos(2 * np.pi * processed['hour']/24)
        
        # Calculate BG momentum (acceleration)
        processed['bg_acceleration'] = processed['bg_trend_5min'].diff()
        
        # Time since last meal
        processed['time_since_meal'] = self._calculate_time_since_meal(processed)
        
        # Calculate variability metrics
        processed['bg_variability'] = self._calculate_bg_variability(processed)

         # Create meal size categories
        processed['meal_size'] = pd.qcut(processed['carbs'], 
                                       q=4, 
                                       labels=['small', 'medium', 'large', 'very_large'])
        
        # One-hot encode categorical variables
        processed = pd.get_dummies(processed, columns=['meal_size'])

        return processed
    
    def _calculate_time_since_meal(self, df):
        """Calculate minutes since last meal"""
        meal_times = df[df['carbs'] > 0]['timestamp']
        times = pd.to_datetime(df['timestamp'])
        
        time_since_meal = []
        for time in times:
            previous_meals = meal_times[meal_times < time]
            if len(previous_meals) > 0:
                minutes = (time - previous_meals.max()).total_seconds() / 60
                time_since_meal.append(minutes)
            else:
                time_since_meal.append(360)  # 6 hours if no previous meal
        
        return time_since_meal
    

    def _calculate_bg_variability(self, df, window=12):
        """Calculate rolling blood glucose variability"""
        return df['blood_glucose'].rolling(window=window).std()
    

    def scale_features(self, features):
        """Scale numerical features"""
        return self.scaler.fit_transform(features)
    

    def prepare_single_prediction(self, current_data):
        """Prepare features for a single prediction"""
        features = pd.DataFrame([current_data])
        processed = self.prepare_features(features)
        
        return self.scale_features(processed[self.config.FEATURE_COLUMNS])