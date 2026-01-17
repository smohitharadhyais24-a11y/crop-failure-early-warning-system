import numpy as np
import pandas as pd
from backend.utils.helpers import setup_logger, log_step, mock_ndvi_data

logger = setup_logger(__name__)

class MODISIngestion:
    """Fetch NDVI data from NASA MODIS satellite (MOD13Q1 product)."""
    
    def __init__(self):
        self.base_url = "https://lpdaac.usgs.gov/products/mod13q1v006/"
        self.resolution = "250m"
    
    def fetch_ndvi_timeseries(self, district, crop, season):
        """
        Fetch 16-day interval NDVI values for a district.
        In production: Use AppEEARS API or Google Earth Engine.
        """
        try:
            log_step("MODIS - NDVI Fetch", "success (mock)")
            return mock_ndvi_data(district, crop, season)
        except Exception as e:
            logger.warning(f"MODIS fetch failed: {e}. Using mock data.")
            return mock_ndvi_data(district, crop, season)

def get_ndvi_data(district, crop, season):
    """Public interface for NDVI data."""
    modis = MODISIngestion()
    return modis.fetch_ndvi_timeseries(district, crop, season)

def extract_ndvi_features(ndvi_data):
    """Extract statistical features from NDVI time-series."""
    values = np.array(ndvi_data['values'])
    
    return {
        'ndvi_mean': np.mean(values),
        'ndvi_trend': ndvi_data['trend'],
        'ndvi_variance': np.var(values),
        'ndvi_min': np.min(values),
        'ndvi_max': np.max(values)
    }
