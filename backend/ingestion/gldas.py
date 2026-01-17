import numpy as np
from backend.utils.helpers import setup_logger, log_step

logger = setup_logger(__name__)

class GLDASIngestion:
    """Fetch soil moisture data from NASA GLDAS."""
    
    def fetch_soil_moisture(self, district):
        """
        Fetch monthly soil moisture values.
        In production: Use GLDAS API via GES DISC.
        """
        log_step("GLDAS - Soil Moisture", "success (mock)")
        return np.random.uniform(20, 80)

def get_soil_moisture(district):
    """Public interface for soil moisture."""
    gldas = GLDASIngestion()
    return {
        'soil_moisture_index': gldas.fetch_soil_moisture(district),
        'soil_moisture_trend': np.random.uniform(-5, 5)
    }
