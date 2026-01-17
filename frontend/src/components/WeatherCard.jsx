import React from 'react';
import { Cloud } from 'lucide-react';

function WeatherCard({ rawFeatures }) {
  const temperature = rawFeatures?.temperature || 25;
  const rainfall = rawFeatures?.rainfall || 50;
  const humidity = rawFeatures?.humidity || 60;
  const tempAnomaly = rawFeatures?.temperature_anomaly || 0;
  const rainfallDev = rawFeatures?.rainfall_deviation || 0;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Cloud size={20} className="text-blue-600" />
        Weather Summary
      </h3>

      <div className="space-y-4">
        {/* Temperature */}
        <div className="p-3 bg-blue-50 rounded-lg">
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium text-gray-700">Temperature</span>
            <span className="text-lg font-bold text-blue-600">{temperature.toFixed(1)}°C</span>
          </div>
          <div className="text-xs text-gray-600">
            Anomaly: {tempAnomaly > 0 ? '+' : ''}{tempAnomaly.toFixed(1)}°C
          </div>
        </div>

        {/* Rainfall */}
        <div className="p-3 bg-cyan-50 rounded-lg">
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium text-gray-700">Rainfall</span>
            <span className="text-lg font-bold text-cyan-600">{rainfall.toFixed(1)} mm</span>
          </div>
          <div className="text-xs text-gray-600">
            Deviation: {rainfallDev > 0 ? '+' : ''}{rainfallDev.toFixed(1)}%
          </div>
        </div>

        {/* Humidity */}
        <div className="p-3 bg-teal-50 rounded-lg">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-gray-700">Humidity</span>
            <span className="text-lg font-bold text-teal-600">{humidity.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
        💡 {rainfallDev < -20 ? 'Rainfall deficit detected' : rainfallDev > 20 ? 'Excess rainfall risk' : 'Normal rainfall patterns'}
      </div>
    </div>
  );
}

export default WeatherCard;
