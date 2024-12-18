import numpy as np
from datetime import datetime
from .config import Config

class InsulinCalculator:
    """ This function handles insulin-related calculations including insulin-on-board (IOB) and will suggest the optimal dosing."""
    def __init__(self):
        self.config = Config()

    def calculate_insulin_on_board(self, insulin_history):
        """This function calculates active insulin using exponential decay
        
        Arguments:
            insulin_history: the dataframe with columns ['timestamp', 'dose']

        Returns:
            a float: current insulin-on-board (IOB)
        """

        current_time = datetime.now()
        active_insulin = 0.0  # this is just for the variable, actual IOB may vary and be added to this

        for _, bolus in insulin_history.iterrows():
            time_diff = (current_time - bolus['timestamp']).total_hours()
            

            if time_diff <= self.config.Insulin_duration:
                # Exponential decal model
                remaining_fraction = np.exp(-time_diff / (self.config.Insulin_duration / 2))
                active_insulin += bolus['dose'] * remaining_fraction
        
        return active_insulin
    
    def calculate_correction_dose(self, current_bg):
        """This function calculates the insulin needed to reach target BG (set in config params)"""

        if current_bg <= self.config.Target_BG:
            return 0.0
        
        correction = (current_bg - self.config.Target_BG) / self.config.Insulin_sensitivity_factor
        return max(0, correction)
    
    def calculate_meal_dose(self, carbs):
        """This function calculates the insulin needed for carbohydrates"""
        return carbs / self.config.Insulin_to_carb_ratio
    
    def adjust_for_trend(self, base_dose, bg_trend):
        """This function adjusts the insulin dosing based on BG trend
        
        Arguments:
                    base_dose: is initial calculated dose
                    bg_trend: Rate of BG change (in mg/dL per min)
        """
        if abs(bg_trend) > self.config.Max_BG_rate_change:
            # Limit the extreme adjustments
            bg_trend = np.clip(bg_trend,
                               -self.config.Max_BG_rate_change,
                               self.config.Max_BG_rate_change)
            
        trend_adjustment = bg_trend * 0.5   # adjust factor based on testing
        adjusted_dose = base_dose + trend_adjustment

        return np.clip(adjusted_dose,
                       self.config.Min_Insulin_Dose,
                       self.config.Max_Insulin_Dose)
            
