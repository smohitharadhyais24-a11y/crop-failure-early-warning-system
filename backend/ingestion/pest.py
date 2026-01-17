import random
from backend.utils.helpers import setup_logger, log_step

logger = setup_logger(__name__)

class PestIngestion:
    """Fetch pest incident data from State Agricultural Department."""
    
    def fetch_pest_records(self, district, season):
        """
        Fetch seasonal pest incident counts.
        In production: Query state agricultural databases.
        """
        log_step("Pest Records Database", "success (mock)")
        
        return {
            'pest_count': random.randint(0, 10),
            'major_pests': random.sample(
                ['Aphids', 'Armyworm', 'Whiteflies', 'Grasshoppers', 'Beetles'],
                k=random.randint(1, 3)
            )
        }

def get_pest_data(district, season):
    """Public interface for pest data."""
    pest_ing = PestIngestion()
    pest_records = pest_ing.fetch_pest_records(district, season)
    
    return {
        'pest_count': pest_records['pest_count'],
        'pest_frequency': pest_records['pest_count'] / 10.0  # Normalize
    }
