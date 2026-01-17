import React, { useState, useEffect } from 'react';
import { Sprout, TrendingUp } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const CropRecommendations = ({ season, soilType, rawFeatures, weather }) => {
  const { t } = useTranslation();
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (season && rawFeatures && weather) {
      fetchRecommendations();
    }
  }, [season, soilType, rawFeatures, weather]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/recommend-crops', {
        season,
        soil_type: soilType,
        raw_features: rawFeatures,
        weather
      });
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Failed to fetch crop recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-300 rounded w-1/3 mb-4"></div>
          <div className="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <Sprout className="text-purple-600" size={24} />
        <h3 className="text-lg font-semibold text-gray-900">{t('risk.cropRecommendations')}</h3>
      </div>

      <div className="space-y-3">
        {recommendations.map((rec, index) => (
          <div
            key={index}
            className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4 border border-purple-200"
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">
                  {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                </span>
                <span className="font-bold text-gray-800 text-lg">{rec.crop}</span>
              </div>
              <div className="bg-purple-100 px-3 py-1 rounded-full">
                <span className="text-purple-700 font-semibold text-sm">
                  {rec.success_probability}% success
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600 italic">{rec.reason}</p>
          </div>
        ))}
      </div>

      <div className="mt-4 bg-blue-50 border border-blue-200 rounded p-3">
        <p className="text-xs text-blue-800">
          💡 <strong>Tip:</strong> These recommendations are based on current soil, weather, and seasonal conditions. Consult local experts before making crop changes.
        </p>
      </div>
    </div>
  );
};

export default CropRecommendations;
