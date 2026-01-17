import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Leaf } from 'lucide-react';

function NDVIChart({ rawFeatures }) {
  // Generate mock NDVI trend data
  const data = Array.from({ length: 8 }, (_, i) => ({
    name: `Week ${i + 1}`,
    ndvi: Math.max(0.2, (rawFeatures?.ndvi_mean || 0.5) + (i - 4) * 0.03 + Math.random() * 0.05)
  }));

  const ndviHealth = rawFeatures?.ndvi_mean >= 0.5 ? 'Healthy' : rawFeatures?.ndvi_mean >= 0.3 ? 'Moderate' : 'Stressed';
  const healthColor = rawFeatures?.ndvi_mean >= 0.5 ? 'text-green-600' : rawFeatures?.ndvi_mean >= 0.3 ? 'text-yellow-600' : 'text-red-600';

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <Leaf size={20} className="text-green-600" />
        Vegetation Health (NDVI)
      </h3>
      
      <div className="mb-4 p-4 bg-green-50 rounded">
        <p className="text-sm text-gray-600">NDVI Mean</p>
        <p className={`text-2xl font-bold ${healthColor}`}>{(rawFeatures?.ndvi_mean || 0.5).toFixed(3)}</p>
        <p className={`text-sm mt-1 ${healthColor}`}>Status: {ndviHealth}</p>
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="name" stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" domain={[0, 1]} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px' }}
            formatter={(value) => value.toFixed(3)}
          />
          <Line 
            type="monotone" 
            dataKey="ndvi" 
            stroke="#22c55e" 
            strokeWidth={2}
            dot={{ fill: '#22c55e', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <p className="text-xs text-gray-500 mt-3">
        Trend: {rawFeatures?.ndvi_trend > 0 ? '↑ Improving' : '↓ Declining'}
      </p>
    </div>
  );
}

export default NDVIChart;
