import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

function Explanation({ explanation }) {
  if (!explanation) return null;

  const factors = explanation.top_factors || [];
  const chartData = factors.map((f, i) => ({
    name: `Factor ${i + 1}`,
    label: f.factor,
    contribution: Math.abs(f.contribution * 100)
  }));

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <TrendingUp size={20} className="text-indigo-600" />
        Why This Risk? - Contributing Factors
      </h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Feature Importance Chart */}
        <div>
          <h4 className="font-medium text-gray-700 mb-3">Top Contributing Factors</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px' }}
                labelFormatter={(value) => `Factor ${value + 1}`}
                formatter={(value) => value.toFixed(1) + '%'}
              />
              <Bar dataKey="contribution" fill="#6366f1" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Factor Details */}
        <div>
          <h4 className="font-medium text-gray-700 mb-3">Factor Details</h4>
          <div className="space-y-3">
            {factors.map((factor, index) => (
              <div key={index} className="p-3 bg-indigo-50 border border-indigo-200 rounded-lg">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-gray-800">{factor.factor}</p>
                    <p className="text-xs text-gray-600 mt-1">
                      Impact: {(Math.abs(factor.contribution) * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="text-2xl">
                    {factor.contribution > 0 ? '📈' : '📉'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="mt-6 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg">
        <h4 className="font-semibold text-gray-800 mb-2">📋 Summary</h4>
        <p className="text-sm text-gray-700">
          Based on satellite NDVI, weather patterns, soil conditions, and pest data, 
          the model predicts a <strong>{(explanation.risk_probability * 100).toFixed(1)}% probability</strong> of crop failure. 
          The above factors are the primary drivers of this prediction.
        </p>
      </div>
    </div>
  );
}

export default Explanation;
