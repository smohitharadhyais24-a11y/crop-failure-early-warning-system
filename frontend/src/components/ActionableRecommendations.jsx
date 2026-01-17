import React, { useState, useEffect } from 'react';
import { CheckCircle2, AlertTriangle, Clock } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const ActionableRecommendations = ({ prediction, weather, soil, ndvi }) => {
  const { t } = useTranslation();
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (prediction && weather && soil && ndvi) {
      fetchRecommendations();
    }
  }, [prediction, weather, soil, ndvi]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/get-recommendations', {
        prediction,
        weather,
        soil,
        ndvi
      });
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-300 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) return null;

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Critical': return 'border-red-300 bg-red-50';
      case 'High': return 'border-orange-300 bg-orange-50';
      case 'Medium': return 'border-yellow-300 bg-yellow-50';
      case 'Low': return 'border-green-300 bg-green-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'Critical': return 'bg-red-600 text-white';
      case 'High': return 'bg-orange-600 text-white';
      case 'Medium': return 'bg-yellow-600 text-white';
      case 'Low': return 'bg-green-600 text-white';
      default: return 'bg-gray-600 text-white';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <CheckCircle2 className="text-indigo-600" size={24} />
        <h3 className="text-lg font-semibold text-gray-900">{t('risk.recommendations')}</h3>
      </div>

      <div className="space-y-4">
        {recommendations.map((rec, index) => (
          <div
            key={index}
            className={`border-2 rounded-lg p-4 ${getPriorityColor(rec.priority)}`}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{rec.icon}</span>
                <div>
                  <div className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${getPriorityBadge(rec.priority)}`}>
                    {rec.priority}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-1 text-xs text-gray-600">
                <Clock size={14} />
                <span>{rec.urgency}</span>
              </div>
            </div>

            <h4 className="font-bold text-gray-800 text-base mb-2">{rec.action}</h4>
            
            <div className="space-y-2 text-sm">
              <div>
                <span className="font-semibold text-gray-700">Details: </span>
                <span className="text-gray-600">{rec.details}</span>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Impact: </span>
                <span className="text-gray-600">{rec.impact}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg p-4">
        <p className="text-sm text-indigo-900 font-semibold mb-2">
          📞 Need Expert Help?
        </p>
        <p className="text-xs text-indigo-800">
          Contact your local Agricultural Extension Office: <strong>1800-180-1551</strong> (Toll-Free)<br />
          Or visit your nearest Krishi Vigyan Kendra (KVK) for personalized guidance.
        </p>
      </div>
    </div>
  );
};

export default ActionableRecommendations;
