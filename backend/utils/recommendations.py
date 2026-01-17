"""
Actionable Recommendations Engine
Provides specific actions based on risk factors
"""

def generate_recommendations(prediction, weather_data, soil_data, ndvi_data):
    """Generate actionable recommendations based on risk analysis"""
    recommendations = []
    
    risk_level = prediction.get('risk_level', 'Low')
    factors = prediction.get('top_factors', [])
    
    # Extract key metrics
    ndvi = ndvi_data.get('ndvi', 0.5)
    soil_moisture = soil_data.get('moisture_percent', 50)
    temperature = weather_data.get('temperature', 28)
    rainfall = weather_data.get('rainfall_7days', 10)
    
    # NDVI-based recommendations
    if ndvi < 0.3:
        recommendations.append({
            'priority': 'Critical',
            'action': 'Apply NPK fertilizer immediately',
            'details': 'Apply 20-25 kg NPK (19:19:19) per hectare within 3 days',
            'impact': 'Improves vegetation health by 30-40% in 2 weeks',
            'urgency': 'Immediate',
            'icon': '🌱'
        })
        recommendations.append({
            'priority': 'High',
            'action': 'Spray micronutrient solution',
            'details': 'Foliar spray with Zinc Sulphate (0.5%) + Ferrous Sulphate (1%)',
            'impact': 'Corrects nutrient deficiency, improves chlorophyll',
            'urgency': 'Within 5 days',
            'icon': '💊'
        })
    elif ndvi < 0.5:
        recommendations.append({
            'priority': 'High',
            'action': 'Top-dressing with Urea',
            'details': 'Apply 10-15 kg Urea per hectare as top-dressing',
            'impact': 'Boosts nitrogen levels, improves greenness',
            'urgency': 'Within 1 week',
            'icon': '🌾'
        })
    
    # Soil moisture recommendations
    if soil_moisture < 30:
        recommendations.append({
            'priority': 'Critical',
            'action': 'Increase irrigation immediately',
            'details': 'Irrigate 2-3 times per week with 25-30mm water per application',
            'impact': 'Prevents water stress and wilting',
            'urgency': 'Immediate',
            'icon': '💧'
        })
        recommendations.append({
            'priority': 'Medium',
            'action': 'Apply mulching',
            'details': 'Use organic mulch (straw/leaves) 5-7cm thick around plants',
            'impact': 'Reduces water evaporation by 50-60%',
            'urgency': 'Within 3 days',
            'icon': '🍂'
        })
    elif soil_moisture > 80:
        recommendations.append({
            'priority': 'High',
            'action': 'Improve drainage',
            'details': 'Create drainage channels to prevent waterlogging',
            'impact': 'Prevents root rot and fungal diseases',
            'urgency': 'Within 2 days',
            'icon': '🚰'
        })
    
    # Temperature-based recommendations
    if temperature > 35:
        recommendations.append({
            'priority': 'High',
            'action': 'Provide shade protection',
            'details': 'Install shade nets (50% shading) or use crop covers',
            'impact': 'Reduces heat stress, improves photosynthesis',
            'urgency': 'Within 2 days',
            'icon': '☀️'
        })
        recommendations.append({
            'priority': 'Medium',
            'action': 'Increase watering frequency',
            'details': 'Water during early morning (5-7 AM) or evening (6-8 PM)',
            'impact': 'Prevents heat stress and leaf burning',
            'urgency': 'Daily',
            'icon': '🕐'
        })
    elif temperature < 18:
        recommendations.append({
            'priority': 'Medium',
            'action': 'Protect from frost',
            'details': 'Cover crops with plastic sheets during night',
            'impact': 'Prevents frost damage to plants',
            'urgency': 'Daily until temperature rises',
            'icon': '🧊'
        })
    
    # Rainfall-based recommendations
    if rainfall < 5:
        recommendations.append({
            'priority': 'High',
            'action': 'Supplemental irrigation required',
            'details': 'Implement drip irrigation or sprinkler system',
            'impact': 'Ensures adequate water supply during drought',
            'urgency': 'Within 3 days',
            'icon': '💦'
        })
    
    # Pest-based recommendations (from factors)
    for factor in factors:
        if 'pest' in factor.get('name', '').lower():
            recommendations.append({
                'priority': 'Critical',
                'action': 'Apply pesticide immediately',
                'details': 'Spray Chlorpyrifos 20% EC @ 2ml/liter or Profenofos 50% EC @ 2ml/liter',
                'impact': 'Controls pest infestation, prevents crop damage',
                'urgency': 'Within 24 hours',
                'icon': '🐛'
            })
            recommendations.append({
                'priority': 'Medium',
                'action': 'Set up pest traps',
                'details': 'Install pheromone traps @ 5 traps per acre',
                'impact': 'Monitors and reduces pest population',
                'urgency': 'Within 2 days',
                'icon': '🪤'
            })
    
    # High risk general recommendations
    if risk_level == 'High':
        recommendations.append({
            'priority': 'High',
            'action': 'Consult agricultural extension officer',
            'details': 'Contact: Karnataka Krishi Vikas Kendra - 1800-425-1234',
            'impact': 'Get expert guidance on crop management',
            'urgency': 'Within 2 days',
            'icon': '👨‍🌾'
        })
        recommendations.append({
            'priority': 'High',
            'action': 'Consider crop insurance',
            'details': 'Enroll in PM Fasal Bima Yojana for risk coverage',
            'impact': 'Financial protection against crop failure',
            'urgency': 'Within 1 week',
            'icon': '📋'
        })
    
    # Sort by priority
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    # Return top 6 recommendations
    return recommendations[:6]

def get_expert_contacts(state):
    """Get expert contact information by state"""
    contacts = {
        'Karnataka': {
            'extension_office': '1800-425-1234',
            'krishi_vigyan': '080-23456789',
            'emergency': '1800-180-1551'
        },
        'Maharashtra': {
            'extension_office': '1800-233-4567',
            'krishi_vigyan': '022-12345678',
            'emergency': '1800-180-1551'
        },
        'default': {
            'extension_office': '1800-180-1551',
            'krishi_vigyan': 'Contact local KVK',
            'emergency': '1800-180-1551'
        }
    }
    
    return contacts.get(state, contacts['default'])
