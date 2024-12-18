import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
import joblib
from datetime import datetime
from .config import Config

class InsulinPredictor:
    """Machine Learning model for insulin prediction"""
    
    def __init__(self):
        self.config = Config()
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.feature_importance = None
    
    def train(self, X, y):
        """
        Train the model
        
        Args:
            X: Feature matrix
            y: Target insulin doses
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.config.FEATURE_COLUMNS,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        
        return {
            'train_score': train_score,
            'test_score': test_score,
            'cv_scores_mean': cv_scores.mean(),
            'cv_scores_std': cv_scores.std()
        }
    
    def predict(self, features):
        """
        Make insulin dose prediction
        
        Args:
            features: Processed feature matrix
        Returns:
            float: Predicted insulin dose
        """
        prediction = self.model.predict(features)[0]
        
        # Apply safety constraints
        safe_prediction = np.clip(
            prediction,
            self.config.MIN_INSULIN_DOSE,
            self.config.MAX_INSULIN_DOSE
        )
        
        return safe_prediction
    
    def save_model(self, filepath):
        """Save model to file"""
        model_data = {
            'model': self.model,
            'feature_importance': self.feature_importance,
            'timestamp': datetime.now(),
            'config': self.config
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """Load model from file"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.feature_importance = model_data['feature_importance']