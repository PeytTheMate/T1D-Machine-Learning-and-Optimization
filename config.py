class Config:
    # CGM settings
    CGM_API_KEY = ""
    CGM_API_SECRET = "" 

    # Safety Precaution (in insulin units)
    Min_Insulin_Dose = 0.0
    Max_Insulin_Dose = 15.0

    Max_BG_rate_change = 3.0  # in mg/dL per minute

    # personal settings
    Insulin_sensitivity_factor = 50  # 1 unit drops BG by 50 mg/dL
    Insulin_to_carb_ratio = 10      # 1 unit per 10g carbs
    Insulin_duration = 3            # hours
    Target_BG = 100 

    # Model features:
    Feature_Columns = [
        'current_bg',
        'bg_trend_5min',
        'bg_trend_15min',
        'bg_trend_30min',
        'carbs',
        'active_insulin',
        'time_of_day',
        'day_of_week',
        'recent_exercise',
        'pre_meal_bg',
        'stress_level'
    ]




