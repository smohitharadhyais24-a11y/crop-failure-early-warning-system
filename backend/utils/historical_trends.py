"""
Historical Trends Module
Generates historical risk trend data for charts
"""
import numpy as np
from datetime import datetime, timedelta
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

class HistoricalTrendsService:
    """Generate historical risk trend data for visualization."""
    
    def __init__(self):
        self.months_back = 12  # Get 12 months of historical data
    
    def generate_risk_trends(self, state, district, crop, season):
        """
        Generate monthly risk probability trends for the past year.
        In production, this would query real historical data.
        """
        trends = []
        end_date = datetime.now()
        
        # Generate 12 months of historical trend data
        for i in range(self.months_back, 0, -1):
            month_date = end_date - timedelta(days=i*30)
            
            # Simulate risk variation with seasonal patterns
            base_risk = 0.30
            seasonal_factor = 0.15 * np.sin((month_date.month - 6) * np.pi / 6)
            random_noise = np.random.uniform(-0.05, 0.05)
            
            risk_probability = max(0.05, min(0.85, base_risk + seasonal_factor + random_noise))
            
            trends.append({
                'month': month_date.strftime('%b %Y'),
                'risk_probability': round(risk_probability, 3),
                'risk_level': 'High' if risk_probability > 0.6 else 'Moderate' if risk_probability > 0.35 else 'Low'
            })
        
        # Add current prediction
        trends.append({
            'month': end_date.strftime('%b %Y'),
            'risk_probability': None,  # Will be filled from actual prediction
            'risk_level': 'Current'
        })
        
        logger.info(f"Generated {len(trends)} months of historical trends for {district}, {state}")
        return trends
    
    def get_ndvi_trends(self, state, district):
        """Generate historical NDVI trends (vegetation health over time)."""
        trends = []
        end_date = datetime.now()
        
        for i in range(12, 0, -1):
            month_date = end_date - timedelta(days=i*30)
            
            # Simulate NDVI variation (0.2 to 0.8)
            base_ndvi = 0.5
            seasonal_variation = 0.15 * np.sin((month_date.month - 3) * np.pi / 6)
            random_noise = np.random.uniform(-0.05, 0.05)
            
            ndvi_value = max(0.15, min(0.85, base_ndvi + seasonal_variation + random_noise))
            
            trends.append({
                'month': month_date.strftime('%b %Y'),
                'ndvi': round(ndvi_value, 3),
                'status': 'Healthy' if ndvi_value > 0.5 else 'Stressed' if ndvi_value > 0.3 else 'Critical'
            })
        
        return trends
    
    def get_rainfall_trends(self, state, district):
        """Generate historical rainfall trends."""
        trends = []
        end_date = datetime.now()
        
        for i in range(12, 0, -1):
            month_date = end_date - timedelta(days=i*30)
            
            # Simulate rainfall (0 to 300mm)
            base_rainfall = 80
            monsoon_factor = 120 if month_date.month in [6, 7, 8, 9] else 0
            random_variation = np.random.uniform(-30, 50)
            
            rainfall = max(0, base_rainfall + monsoon_factor + random_variation)
            
            trends.append({
                'month': month_date.strftime('%b %Y'),
                'rainfall_mm': round(rainfall, 1)
            })
        
        return trends

def get_historical_data(state, district, crop, season):
    """Public interface to get all historical trends."""
    service = HistoricalTrendsService()
    
    return {
        'risk_trends': service.generate_risk_trends(state, district, crop, season),
        'ndvi_trends': service.get_ndvi_trends(state, district),
        'rainfall_trends': service.get_rainfall_trends(state, district)
    }
