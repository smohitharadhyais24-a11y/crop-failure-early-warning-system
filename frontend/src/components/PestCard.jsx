import React from 'react';
import { Bug } from 'lucide-react';

function PestCard({ rawFeatures }) {
  const pestCount = rawFeatures?.pest_count || 2;
  const pestFrequency = rawFeatures?.pest_frequency || 0.3;

  const getPestRisk = () => {
    if (pestCount <= 2) return { risk: 'Low', color: 'text-green-600', bg: 'bg-green-50' };
    if (pestCount <= 5) return { risk: 'Medium', color: 'text-yellow-600', bg: 'bg-yellow-50' };
    return { risk: 'High', color: 'text-red-600', bg: 'bg-red-50' };
  };

  const pest = getPestRisk();

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Bug size={20} className="text-red-600" />
        Pest & Disease Risk
      </h3>

      <div className="space-y-4">
        {/* Pest Count */}
        <div className={`p-4 ${pest.bg} rounded-lg`}>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Pest Incidents</span>
            <span className={`text-2xl font-bold ${pest.color}`}>{pestCount}</span>
          </div>
          <p className={`text-sm ${pest.color}`}>Risk Level: {pest.risk}</p>
        </div>

        {/* Pest Frequency */}
        <div className="p-4 bg-purple-50 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Frequency Index</span>
            <span className="text-lg font-bold text-purple-600">{(pestFrequency * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="h-2 rounded-full bg-purple-500"
              style={{ width: `${pestFrequency * 100}%` }}
            />
          </div>
        </div>

        {/* Major Pests */}
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-sm font-medium text-gray-700 mb-2">Common Pests</p>
          <div className="flex flex-wrap gap-2">
            {['Aphids', 'Armyworm', 'Beetles'].slice(0, 2).map(pest => (
              <span key={pest} className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">
                {pest}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className={`mt-4 p-3 ${pestCount > 5 ? 'bg-red-50 border border-red-200 text-red-800' : 'bg-green-50 border border-green-200 text-green-800'} rounded text-xs`}>
        🐛 {pestCount > 5 ? 'Implement pest management strategies immediately' : pestCount > 2 ? 'Monitor pest activity regularly' : 'Pest pressure is manageable'}
      </div>
    </div>
  );
}

export default PestCard;
