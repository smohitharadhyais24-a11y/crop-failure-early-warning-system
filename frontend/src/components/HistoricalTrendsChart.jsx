import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Minus, Activity } from 'lucide-react';
import axios from 'axios';

function HistoricalTrendsChart({ state, district, crop, season }) {
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('risk');

  useEffect(() => {
    if (state && district && crop && season) {
      fetchTrends();
    }
  }, [state, district, crop, season]);

  const fetchTrends = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/historical-trends', {
        state,
        district,
        crop,
        season
      });
      setTrends(response.data);
    } catch (error) {
      console.error('Failed to fetch historical trends:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </div>
    );
  }

  if (!trends) {
    return null;
  }

  const renderRiskTrends = () => {
    const data = trends.risk_trends || [];
    const maxRisk = Math.max(...data.map(d => d.risk_probability || 0));
    
    return (
      <div>
        <h4 className="font-semibold text-gray-800 mb-4">Risk Probability Trends (12 Months)</h4>
        <div className="space-y-2">
          {data.map((point, idx) => {
            const height = point.risk_probability ? (point.risk_probability / maxRisk * 100) : 0;
            const color = point.risk_probability > 0.6 ? 'bg-red-500' : 
                         point.risk_probability > 0.35 ? 'bg-yellow-500' : 'bg-green-500';
            
            return (
              <div key={idx} className="flex items-center gap-3">
                <span className="text-xs text-gray-600 w-20">{point.month}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-6 overflow-hidden">
                  <div 
                    className={`h-full ${color} transition-all duration-300 flex items-center justify-end pr-2`}
                    style={{ width: `${height}%` }}
                  >
                    {point.risk_probability && (
                      <span className="text-xs text-white font-semibold">
                        {(point.risk_probability * 100).toFixed(0)}%
                      </span>
                    )}
                  </div>
                </div>
                <span className={`text-xs font-semibold w-16 ${
                  point.risk_level === 'High' ? 'text-red-600' :
                  point.risk_level === 'Moderate' ? 'text-yellow-600' :
                  point.risk_level === 'Low' ? 'text-green-600' : 'text-gray-600'
                }`}>
                  {point.risk_level}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderNDVITrends = () => {
    const data = trends.ndvi_trends || [];
    const maxNDVI = 1.0;
    
    return (
      <div>
        <h4 className="font-semibold text-gray-800 mb-4">Vegetation Health (NDVI) Trends</h4>
        <div className="space-y-2">
          {data.map((point, idx) => {
            const height = (point.ndvi / maxNDVI) * 100;
            const color = point.ndvi > 0.5 ? 'bg-green-500' : 
                         point.ndvi > 0.3 ? 'bg-yellow-500' : 'bg-red-500';
            
            return (
              <div key={idx} className="flex items-center gap-3">
                <span className="text-xs text-gray-600 w-20">{point.month}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-6 overflow-hidden">
                  <div 
                    className={`h-full ${color} transition-all duration-300 flex items-center justify-end pr-2`}
                    style={{ width: `${height}%` }}
                  >
                    <span className="text-xs text-white font-semibold">
                      {point.ndvi.toFixed(2)}
                    </span>
                  </div>
                </div>
                <span className={`text-xs font-semibold w-16 ${
                  point.status === 'Healthy' ? 'text-green-600' :
                  point.status === 'Stressed' ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {point.status}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderRainfallTrends = () => {
    const data = trends.rainfall_trends || [];
    const maxRainfall = Math.max(...data.map(d => d.rainfall_mm));
    
    return (
      <div>
        <h4 className="font-semibold text-gray-800 mb-4">Monthly Rainfall Trends (mm)</h4>
        <div className="space-y-2">
          {data.map((point, idx) => {
            const height = (point.rainfall_mm / maxRainfall) * 100;
            
            return (
              <div key={idx} className="flex items-center gap-3">
                <span className="text-xs text-gray-600 w-20">{point.month}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-6 overflow-hidden">
                  <div 
                    className="h-full bg-blue-500 transition-all duration-300 flex items-center justify-end pr-2"
                    style={{ width: `${height}%` }}
                  >
                    <span className="text-xs text-white font-semibold">
                      {point.rainfall_mm.toFixed(0)}mm
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center gap-2 mb-6">
        <Activity className="text-green-600" size={24} />
        <h3 className="font-bold text-lg text-gray-900">Historical Trends Analysis</h3>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('risk')}
          className={`px-4 py-2 font-semibold transition ${
            activeTab === 'risk'
              ? 'text-green-600 border-b-2 border-green-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Risk Trends
        </button>
        <button
          onClick={() => setActiveTab('ndvi')}
          className={`px-4 py-2 font-semibold transition ${
            activeTab === 'ndvi'
              ? 'text-green-600 border-b-2 border-green-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Vegetation Health
        </button>
        <button
          onClick={() => setActiveTab('rainfall')}
          className={`px-4 py-2 font-semibold transition ${
            activeTab === 'rainfall'
              ? 'text-green-600 border-b-2 border-green-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Rainfall
        </button>
      </div>

      {/* Chart Content */}
      <div className="min-h-[400px]">
        {activeTab === 'risk' && renderRiskTrends()}
        {activeTab === 'ndvi' && renderNDVITrends()}
        {activeTab === 'rainfall' && renderRainfallTrends()}
      </div>

      <div className="mt-4 text-xs text-gray-500 italic">
        * Historical data based on past 12 months of observations
      </div>
    </div>
  );
}

export default HistoricalTrendsChart;
