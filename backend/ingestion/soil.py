import random
from backend.utils.helpers import setup_logger, log_step

logger = setup_logger(__name__)

class SoilIngestion:
    """Fetch soil data from NBSS&LUP Soil Database."""
    
    def fetch_soil_properties(self, district):
        """
        Fetch district-level soil properties.
        In production: Query NBSS&LUP database or use soil maps.
        """
        log_step("NBSS&LUP Soil Database", "success (mock)")
        
        soil_types = ['Sandy Loam', 'Clay Loam', 'Silt Loam', 'Clay', 'Loam']
        
        return {
            'soil_type': random.choice(soil_types),
            'organic_carbon': random.uniform(0.3, 1.5),
            'soil_depth': random.uniform(30, 100)
        }

def get_soil_data(district):
    """Public interface for soil data."""
    soil_ing = SoilIngestion()
    soil_props = soil_ing.fetch_soil_properties(district)
    
    # Encode soil type
    soil_type_encoding = {
        'Sandy Loam': 1,
        'Clay Loam': 2,
        'Silt Loam': 3,
        'Clay': 4,
        'Loam': 5
    }
    
    return {
        'soil_type': soil_props['soil_type'],
        'soil_type_encoded': soil_type_encoding.get(soil_props['soil_type'], 0),
        'organic_carbon': soil_props['organic_carbon'],
        'soil_depth': soil_props['soil_depth']
    }
