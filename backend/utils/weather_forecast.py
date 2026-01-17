"""
Weather Forecast Integration
Fetches 7-day weather forecast and predicts risk for each day
"""
import os
import requests
from datetime import datetime, timedelta

def get_7day_forecast(state, district):
    """Get 7-day weather forecast for a location"""
    api_key = os.getenv('OPENWEATHER_API_KEY', 'YOUR_API_KEY')
    
    # District coordinates (sample - expand as needed)
    coordinates = {
        'Bengaluru Urban': (12.9716, 77.5946),
        'Mysuru': (12.2958, 76.6394),
        'Pune': (18.5204, 73.8567),
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.7041, 77.1025),
    }
    
    lat, lon = coordinates.get(district, (12.9716, 77.5946))
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Process forecast data (API returns 3-hour intervals for 5 days)
        daily_forecasts = []
        current_date = None
        day_data = {'temp_sum': 0, 'temp_count': 0, 'rain_sum': 0, 'humidity_sum': 0, 'humidity_count': 0}
        
        for item in data.get('list', []):
            date = datetime.fromtimestamp(item['dt']).date()
            
            if current_date != date:
                if current_date is not None:
                    # Calculate averages for previous day
                    avg_temp = day_data['temp_sum'] / day_data['temp_count']
                    avg_humidity = day_data['humidity_sum'] / day_data['humidity_count']
                    
                    daily_forecasts.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'temperature': round(avg_temp, 1),
                        'rainfall': round(day_data['rain_sum'], 1),
                        'humidity': round(avg_humidity, 1),
                        'description': day_data.get('description', 'Clear')
                    })
                
                # Reset for new day
                current_date = date
                day_data = {
                    'temp_sum': 0,
                    'temp_count': 0,
                    'rain_sum': 0,
                    'humidity_sum': 0,
                    'humidity_count': 0,
                    'description': item['weather'][0]['description']
                }
            
            # Accumulate data
            day_data['temp_sum'] += item['main']['temp']
            day_data['temp_count'] += 1
            day_data['humidity_sum'] += item['main']['humidity']
            day_data['humidity_count'] += 1
            day_data['rain_sum'] += item.get('rain', {}).get('3h', 0)
        
        return daily_forecasts[:7]  # Return 7 days
        
    except Exception as e:
        print(f"Error fetching forecast: {str(e)}")
        # Return dummy data for demonstration
        return generate_dummy_forecast()

def generate_dummy_forecast():
    """Generate dummy forecast data for testing"""
    forecasts = []
    base_temp = 28
    
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        forecasts.append({
            'date': date,
            'temperature': round(base_temp + (i * 0.5), 1),
            'rainfall': round(5 - (i * 0.5), 1),
            'humidity': round(65 + (i * 2), 1),
            'description': 'Partly cloudy'
        })
    
    return forecasts

def predict_daily_risks(forecast_data, current_ndvi, current_soil_moisture, pest_frequency):
    """Predict risk for each forecasted day"""
    from backend.model.predict import ModelPredictor
    import numpy as np
    
    predictor = ModelPredictor()
    model = predictor.model
    scaler = predictor.scaler
    daily_risks = []
    
    # Historical averages (simulated)
    historical_avg_rainfall = 50
    historical_avg_temp = 27
    
    for day in forecast_data:
        # Calculate deviations
        rainfall_deviation = ((day['rainfall'] - historical_avg_rainfall) / historical_avg_rainfall) * 100
        temp_anomaly = day['temperature'] - historical_avg_temp
        
        # Create feature vector
        features = np.array([[
            current_ndvi,  # Assume NDVI changes slowly
            rainfall_deviation,
            current_soil_moisture,
            temp_anomaly,
            pest_frequency,
            0.05,  # ndvi_trend (assume stable)
            1,  # soil_type_encoded
            1   # season_encoded
        ]])
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        risk_prob = model.predict_proba(features_scaled)[0][1]
        
        if risk_prob >= 0.7:
            risk_level = 'High'
        elif risk_prob >= 0.4:
            risk_level = 'Moderate'
        else:
            risk_level = 'Low'
        
        daily_risks.append({
            'date': day['date'],
            'temperature': day['temperature'],
            'rainfall': day['rainfall'],
            'humidity': day['humidity'],
            'risk_level': risk_level,
            'risk_probability': round(risk_prob * 100, 1)
        })
    
    return daily_risks
