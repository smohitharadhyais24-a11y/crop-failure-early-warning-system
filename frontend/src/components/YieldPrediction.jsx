import React, { useState, useEffect } from 'react';
import { TrendingUp, Info } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const YieldPrediction = ({ crop, rawFeatures }) => {
  const { t } = useTranslation();
  const [yieldData, setYieldData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (crop && rawFeatures) {
      fetchYieldPrediction();
    }
  }, [crop, rawFeatures]);

  const fetchYieldPrediction = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/predict-yield', {
        crop,
        raw_features: rawFeatures
      });
      setYieldData(response.data);
    } catch (error) {
      console.error('Failed to fetch yield prediction:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-300 rounded w-1/3 mb-4"></div>
          <div className="h-24 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!yieldData) return null;

  const isAboveAverage = yieldData.comparison_percent > 0;

  return (
    <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg shadow-md p-6 border border-green-200">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="text-green-600" size={24} />
        <h3 className="text-lg font-semibold text-gray-900">{t('risk.yieldPrediction')}</h3>
      </div>

      <div className="space-y-4">
        <div>
          <div className="text-3xl font-bold text-green-700">
            {yieldData.yield_low} - {yieldData.yield_high}
          </div>
          <div className="text-sm text-gray-600 mt-1">
            {yieldData.unit} ({crop})
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">{t('yield.bestEstimate')}</span>
            <span className="font-semibold text-gray-800">{yieldData.yield_estimate} quintals/ha</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">{t('yield.historicalAverage')}</span>
            <span className="font-semibold text-gray-800">{yieldData.historical_average} quintals/ha</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">{t('yield.comparison')}</span>
            <span className={`font-semibold ${isAboveAverage ? 'text-green-600' : 'text-red-600'}`}>
              {Math.abs(yieldData.comparison_percent)}% {yieldData.comparison_text}
            </span>
          </div>
        </div>

        <div className="flex items-start gap-2 bg-blue-50 border border-blue-200 rounded p-3">
          <Info size={16} className="text-blue-600 mt-0.5 flex-shrink-0" />
          <p className="text-xs text-blue-800">
            {t('yield.note')}
          </p>
        </div>
      </div>
    </div>
  );
};

export default YieldPrediction;
