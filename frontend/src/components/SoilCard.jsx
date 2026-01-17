import React from 'react';
import { Droplets } from 'lucide-react';

function SoilCard({ rawFeatures }) {
  const soilMoisture = rawFeatures?.soil_moisture_index || 0.6;
  const soilType = rawFeatures?.soil_type || 'Loam';
  const organicCarbon = rawFeatures?.organic_carbon || 0.8;

  const getMoistureStatus = () => {
    if (soilMoisture < 0.3) return { status: 'Dry', color: 'text-red-600', bg: 'bg-red-50' };
    if (soilMoisture < 0.6) return { status: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-50' };
    return { status: 'Wet', color: 'text-blue-600', bg: 'bg-blue-50' };
  };

  const moisture = getMoistureStatus();

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Droplets size={20} className="text-blue-600" />
        Soil & Moisture
      </h3>

      <div className="space-y-4">
        {/* Soil Type */}
        <div className="p-3 bg-amber-50 rounded-lg">
          <p className="text-sm font-medium text-gray-700">Soil Type</p>
          <p className="text-lg font-bold text-amber-700 mt-1">{soilType}</p>
        </div>

        {/* Soil Moisture */}
        <div className={`p-3 ${moisture.bg} rounded-lg`}>
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium text-gray-700">Soil Moisture</span>
            <span className={`text-lg font-bold ${moisture.color}`}>{(soilMoisture * 100).toFixed(1)}%</span>
          </div>
          <div className={`text-xs ${moisture.color}`}>
            {moisture.status}
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div 
              className={`h-2 rounded-full transition-all ${moisture.status === 'Dry' ? 'bg-red-500' : moisture.status === 'Moderate' ? 'bg-yellow-500' : 'bg-blue-500'}`}
              style={{ width: `${soilMoisture * 100}%` }}
            />
          </div>
        </div>

        {/* Organic Carbon */}
        <div className="p-3 bg-green-50 rounded-lg">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-gray-700">Organic Carbon</span>
            <span className="text-lg font-bold text-green-600">{organicCarbon.toFixed(2)}%</span>
          </div>
        </div>
      </div>

      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded text-xs text-blue-800">
        💧 {soilMoisture < 0.3 ? 'Irrigation recommended' : soilMoisture > 0.8 ? 'Drainage may be needed' : 'Soil conditions optimal'}
      </div>
    </div>
  );
}

export default SoilCard;
