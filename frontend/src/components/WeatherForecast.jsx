import React, { useState, useEffect } from 'react';
import { TrendingUp, Calendar, ThermometerSun, CloudRain, Droplets } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const WeatherForecast = ({ state, district, rawFeatures }) => {
  const { t } = useTranslation();
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (state && district && rawFeatures) {
      fetchForecast();
    }
  }, [state, district, rawFeatures]);

  const fetchForecast = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/weather-forecast', {
        state,
        district,
        raw_features: rawFeatures
      });
      setForecast(response.data.forecast);
    } catch (error) {
      console.error('Failed to fetch forecast:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-300 rounded w-1/3 mb-4"></div>
          <div className="h-40 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!forecast) return null;

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'High': return 'text-red-600 bg-red-100';
      case 'Moderate': return 'text-yellow-600 bg-yellow-100';
      case 'Low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <Calendar className="text-blue-600" size={24} />
        <h3 className="text-lg font-semibold text-gray-900">{t('risk.forecast')}</h3>
      </div>

      <div className="overflow-x-auto">
        <div className="flex gap-4 min-w-max">
          {forecast.map((day, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-4 min-w-[140px] border border-gray-200"
            >
              <div className="text-center mb-3">
                <div className="text-sm font-semibold text-gray-700">
                  {index === 0 ? t('weather.today') : index === 1 ? t('weather.tomorrow') : `${t('weather.day')} ${index + 1}`}
                </div>
                <div className="text-xs text-gray-500">
                  {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <ThermometerSun size={16} className="text-orange-500" />
                  <span className="text-gray-700">{day.temperature}°C</span>
                </div>
                <div className="flex items-center gap-2">
                  <CloudRain size={16} className="text-blue-500" />
                  <span className="text-gray-700">{day.rainfall}mm</span>
                </div>
                <div className="flex items-center gap-2">
                  <Droplets size={16} className="text-cyan-500" />
                  <span className="text-gray-700">{day.humidity}%</span>
                </div>
              </div>

              <div className={`mt-3 px-2 py-1 rounded text-xs font-semibold text-center ${getRiskColor(day.risk_level)}`}>
                {day.risk_level} ({day.risk_probability}%)
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WeatherForecast;
