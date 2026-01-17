import React, { useState } from 'react';
import { Cloud, Droplets, Sprout, AlertTriangle, CheckCircle, TrendingDown, Download, FileText, Info } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import HistoricalTrendsChart from './HistoricalTrendsChart';
import ModelInfoModal from './ModelInfoModal';
import SatelliteMap from './SatelliteMap';
import WeatherForecast from './WeatherForecast';
import YieldPrediction from './YieldPrediction';
import CropRecommendations from './CropRecommendations';
import ActionableRecommendations from './ActionableRecommendations';
import axios from 'axios';

function DashboardContent({ prediction, loading, error, selectedValues }) {
  const { t } = useTranslation();
  const [exportingPDF, setExportingPDF] = useState(false);
  const [showModelInfo, setShowModelInfo] = useState(false);

  const handleExportPDF = async () => {
    setExportingPDF(true);
    try {
      const response = await axios.post('/api/export-pdf', {
        prediction_data: {
          state: selectedValues.state,
          district: selectedValues.district,
          crop: selectedValues.crop,
          season: selectedValues.season,
          ...prediction
        }
      }, {
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `CFEWS_Report_${selectedValues.state}_${selectedValues.district}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('PDF export failed:', error);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setExportingPDF(false);
    }
  };
  if (loading) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin">
            <div className="w-16 h-16 border-4 border-green-200 border-t-green-600 rounded-full"></div>
          </div>
          <p className="mt-4 text-gray-600 font-semibold">{t('loading.analyzing')}</p>
          <p className="text-sm text-gray-500 mt-1">{t('loading.fetching')}</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6 max-w-md text-center">
          <AlertTriangle className="text-red-600 mx-auto mb-3" size={32} />
          <h3 className="font-bold text-red-900 text-lg mb-2">{t('dashboard.analysisErrorTitle')}</h3>
          <p className="text-red-700 mb-4">{error}</p>
          <p className="text-sm text-red-600">{t('dashboard.analysisErrorMessage')}</p>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="text-center">
          <Sprout className="text-green-600 mx-auto mb-4" size={48} />
          <h3 className="font-bold text-xl text-gray-900 mb-2">{t('risk.selectDetails')}</h3>
          <p className="text-gray-600 mb-4">{t('dashboard.fillForm')}</p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left text-sm">
            <p className="font-semibold text-blue-900 mb-2">{t('risk.whatYouGet')}</p>
            <ul className="space-y-1 text-blue-800">
              <li>✓ {t('dashboard.riskAssessment')}</li>
              <li>✓ {t('dashboard.cropRecommendation')}</li>
              <li>✓ {t('dashboard.weatherAdvisory')}</li>
              <li>✓ {t('dashboard.riskBreakdown')}</li>
              <li>✓ {t('dashboard.liveData')}</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  const riskData = [
    { factor: 'NDVI', value: prediction.raw_features?.ndvi_mean || 0.4 },
    { factor: 'Rainfall Dev', value: Math.min(Math.abs(prediction.raw_features?.rainfall_deviation || 0) / 5, 1) },
    { factor: 'Soil Moisture', value: Math.min((prediction.raw_features?.soil_moisture_index || 50) / 100, 1) },
    { factor: 'Temp Anomaly', value: Math.min(Math.abs(prediction.raw_features?.temperature_anomaly || 0) / 3, 1) }
  ];

  const localizedRiskLevel = prediction.risk_level
    ? t(`risk.${prediction.risk_level.toLowerCase()}`, { defaultValue: prediction.risk_level })
    : t('risk.low');

  return (
    <div className="flex-1 overflow-y-auto">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-8 sticky top-0 z-10 shadow-md">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold mb-2">{t('dashboard.riskAnalysis')}</h2>
            <p className="text-green-100">
              {selectedValues.district}, {selectedValues.state} • {selectedValues.crop} • {selectedValues.season}
            </p>
          </div>
          <button
            onClick={handleExportPDF}
            disabled={exportingPDF}
            className="bg-white text-green-600 px-6 py-3 rounded-lg font-bold hover:bg-green-50 transition flex items-center gap-2 shadow-lg disabled:opacity-50"
          >
            {exportingPDF ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
                {t('actions.exporting')}
              </>
            ) : (
              <>
                <Download size={20} />
                {t('actions.exportPDF')}
              </>
            )}
          </button>
        </div>
      </div>

      <div className="p-8 space-y-8">
        {/* Risk Level Card with Confidence */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className={`p-6 rounded-lg shadow-md text-center border-l-4 ${
            prediction.risk_level === 'High' ? 'bg-red-50 border-red-600' :
            prediction.risk_level === 'Moderate' ? 'bg-yellow-50 border-yellow-600' :
            'bg-green-50 border-green-600'
          }`}>
            <div className={`text-4xl font-bold mb-2 ${
              prediction.risk_level === 'High' ? 'text-red-600' :
              prediction.risk_level === 'Moderate' ? 'text-yellow-600' :
              'text-green-600'
            }`}>
              {localizedRiskLevel}
            </div>
            <p className="text-gray-700 font-semibold">{t('dashboard.cropFailureRisk')}</p>
            <div className="mt-3 text-2xl font-bold">
              {(prediction.probability * 100).toFixed(1)}%
            </div>
            <p className="text-sm text-gray-600 mb-3">{t('dashboard.failureProbability')}</p>
            
            {/* Confidence Score */}
            {prediction.confidence !== undefined && (
              <div className="mt-4 pt-4 border-t border-gray-300">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-600">{t('risk.confidence')}</span>
                  <span className="text-sm font-bold">{(prediction.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${
                      prediction.confidence > 0.7 ? 'bg-green-500' : 
                      prediction.confidence > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${prediction.confidence * 100}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {prediction.explanation?.confidence_level || t('risk.moderate')} {t('risk.confidence')}
                </p>
              </div>
            )}
          </div>

          {/* Weather Card */}
          <div className="p-6 rounded-lg shadow-md bg-blue-50 border-l-4 border-blue-600">
            <div className="flex items-center gap-3 mb-4">
              <Cloud className="text-blue-600" size={24} />
              <h4 className="font-bold text-gray-900">{t('dashboard.liveWeather')}</h4>
            </div>
            <div className="space-y-2">
              <div><span className="text-sm text-gray-600">{t('dashboard.temperature')}:</span> <span className="font-bold">28.5°C</span></div>
              <div><span className="text-sm text-gray-600">{t('dashboard.rainfall')}:</span> <span className="font-bold">45mm</span></div>
              <div><span className="text-sm text-gray-600">{t('dashboard.humidity')}:</span> <span className="font-bold">72%</span></div>
            </div>
          </div>

          {/* Soil Card */}
          <div className="p-6 rounded-lg shadow-md bg-amber-50 border-l-4 border-amber-600">
            <div className="flex items-center gap-3 mb-4">
              <Droplets className="text-amber-600" size={24} />
              <h4 className="font-bold text-gray-900">{t('dashboard.soilStatus')}</h4>
            </div>
            <div className="space-y-2">
              <div><span className="text-sm text-gray-600">{t('dashboard.moisture')}:</span> <span className="font-bold">54%</span></div>
              <div><span className="text-sm text-gray-600">{t('dashboard.pH')}:</span> <span className="font-bold">6.8</span></div>
              <div><span className="text-sm text-gray-600">{t('dashboard.status')}:</span> <span className="font-bold text-green-600">{t('dashboard.healthy')}</span></div>
            </div>
          </div>
        </div>

        {/* Risk Breakdown with Interpretations */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
            <AlertTriangle size={20} className="text-orange-600" />
            {t('dashboard.topRiskFactors')}
          </h3>
          <div className="space-y-4">
            {prediction.explanation?.top_factors?.slice(0, 5).map((factor, idx) => (
              <div key={idx} className="border-l-4 border-orange-400 pl-4 py-2 bg-orange-50 rounded-r">
                <div className="flex justify-between items-start mb-1">
                  <div className="flex-1">
                    <span className="text-sm font-bold text-gray-900">#{idx + 1} {factor.factor}</span>
                    {factor.interpretation && (
                      <p className="text-xs text-gray-600 mt-1 italic">{factor.interpretation}</p>
                    )}
                  </div>
                  <span className="text-sm font-bold text-orange-600 ml-4">
                    {(Math.abs(factor.contribution) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full mt-2">
                  <div
                    className={`h-full rounded-full ${
                      Math.abs(factor.contribution) > 0.15 ? 'bg-red-500' :
                      Math.abs(factor.contribution) > 0.10 ? 'bg-orange-500' :
                      'bg-yellow-500'
                    }`}
                    style={{ width: `${Math.min(Math.abs(factor.contribution) * 400, 100)}%` }}
                  ></div>
                </div>
              </div>
            )) || riskData.map((factor, idx) => (
              <div key={idx}>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-semibold text-gray-700">{factor.factor}</span>
                  <span className="text-sm font-bold text-orange-600">{(factor.value * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full">
                  <div
                    className="h-full bg-gradient-to-r from-orange-400 to-orange-600 rounded-full"
                    style={{ width: `${factor.value * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
          
          {/* Model Accuracy Badge */}
          {prediction.model_accuracy && (
            <div className="mt-4 pt-4 border-t border-gray-200 text-center">
              <span className="text-xs text-gray-600">{t('dashboard.modelAccuracy')}: </span>
              <span className="text-sm font-bold text-green-600">
                {(prediction.model_accuracy * 100).toFixed(1)}%
              </span>
            </div>
          )}
        </div>

        {/* Risk Explanation */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="font-bold text-lg text-gray-900 mb-4">{t('dashboard.whyThisRisk')}</h3>
          <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded space-y-3">
            {prediction.explanation?.top_factors ? (
              <>
                <p className="text-gray-800 font-semibold">{t('dashboard.topContributing')}</p>
                <ul className="space-y-2">
                  {prediction.explanation.top_factors.map((factor, idx) => (
                    <li key={idx} className="flex items-center justify-between text-gray-700">
                      <span>• {factor.factor}</span>
                      <span className="font-bold text-orange-600">{(factor.contribution * 100).toFixed(1)}%</span>
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <p className="text-gray-800">{prediction.explanation || t('dashboard.analysisComplete')}</p>
            )}
          </div>
        </div>

        {/* Crop Suitability Recommendations */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
            <Sprout size={20} className="text-green-600" />
            {t('dashboard.alternativeCrops')}
          </h3>
          <div className="space-y-3">
            {[
              { name: t('crop.millet'), suitability: t('dashboard.highSuitability'), score: 0.85 },
              { name: t('crop.soybean'), suitability: t('dashboard.highSuitability'), score: 0.82 },
              { name: t('crop.cotton'), suitability: t('dashboard.moderateSuitability'), score: 0.68 },
              { name: t('crop.sugarcane'), suitability: t('dashboard.lowSuitability'), score: 0.45 }
            ].map((crop, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900">{crop.name}</p>
                  <p className={`text-sm ${
                    crop.suitability === t('dashboard.highSuitability') ? 'text-green-600' :
                    crop.suitability === t('dashboard.moderateSuitability') ? 'text-yellow-600' :
                    'text-red-600'
                  }`}>{crop.suitability}</p>
                </div>
                <div className="w-16 h-2 bg-gray-200 rounded-full">
                  <div
                    className={`h-full rounded-full ${
                      crop.suitability === 'High' ? 'bg-green-500' :
                      crop.suitability === 'Moderate' ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}
                    style={{ width: `${crop.score * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Weather Advisory */}
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-orange-600">
          <h3 className="font-bold text-lg text-gray-900 mb-4">⚠️ {t('dashboard.weatherAdvisoryTitle')}</h3>
          <ul className="space-y-3">
            <li className="flex gap-3 text-gray-800">
              <span className="text-orange-600 font-bold">•</span>
              <span>{t('dashboard.weatherNote1')}</span>
            </li>
            <li className="flex gap-3 text-gray-800">
              <span className="text-orange-600 font-bold">•</span>
              <span>{t('dashboard.weatherNote2')}</span>
            </li>
            <li className="flex gap-3 text-gray-800">
              <span className="text-orange-600 font-bold">•</span>
              <span>{t('dashboard.weatherNote3')}</span>
            </li>
          </ul>
        </div>

        {/* NEW FEATURES SECTION */}
        
        {/* Actionable Recommendations */}
        <ActionableRecommendations
          prediction={prediction}
          weather={{
            temperature: prediction.raw_features?.temperature || 28,
            rainfall: prediction.raw_features?.rainfall_7days || 10,
            humidity: prediction.raw_features?.humidity || 65
          }}
          soil={{
            moisture_percent: (prediction.raw_features?.soil_moisture_index || 50),
            type: selectedValues.soilType
          }}
          ndvi={{
            ndvi: prediction.raw_features?.ndvi_mean || 0.5
          }}
        />

        {/* 7-Day Weather Forecast */}
        <WeatherForecast
          state={selectedValues.state}
          district={selectedValues.district}
          rawFeatures={prediction.raw_features}
        />

        {/* Yield Prediction & Crop Recommendations Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <YieldPrediction
            crop={selectedValues.crop}
            rawFeatures={prediction.raw_features}
          />
          <CropRecommendations
            season={selectedValues.season}
            soilType={selectedValues.soilType}
            rawFeatures={prediction.raw_features}
            weather={{
              temperature: prediction.raw_features?.temperature || 28
            }}
          />
        </div>

        {/* Satellite Map Button */}
        <div className="flex justify-center">
          <SatelliteMap
            district={selectedValues.district}
            state={selectedValues.state}
            ndviValue={prediction.raw_features?.ndvi_mean || 0.5}
          />
        </div>

        {/* Historical Trends Chart */}
        <HistoricalTrendsChart 
          state={selectedValues.state}
          district={selectedValues.district}
          crop={selectedValues.crop}
          season={selectedValues.season}
        />

        {/* Data Sources & Credits */}
        <div className="bg-gradient-to-r from-gray-100 to-gray-50 p-6 rounded-lg shadow-md border-t-2 border-gray-300">
          <h3 className="font-bold text-lg text-gray-900 mb-4">📊 {t('dashboard.dataSources')}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="flex gap-3">
              <span className="text-blue-600 font-bold">🌡️</span>
              <div>
                <p className="font-semibold text-gray-900">OpenWeather API</p>
                <p className="text-gray-600">{t('weather.liveWeatherData')}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-green-600 font-bold">🛰️</span>
              <div>
                <p className="font-semibold text-gray-900">NASA MODIS</p>
                <p className="text-gray-600">{t('model.satelliteNdvi')}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-cyan-600 font-bold">💧</span>
              <div>
                <p className="font-semibold text-gray-900">NASA GLDAS</p>
                <p className="text-gray-600">{t('soil.soilMoisture')}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-purple-600 font-bold">🌱</span>
              <div>
                <p className="font-semibold text-gray-900">NBSS&LUP</p>
                <p className="text-gray-600">{t('model.soilComposition')}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-red-600 font-bold">🏛️</span>
              <div>
                <p className="font-semibold text-gray-900">{t('model.ministry')}</p>
                <p className="text-gray-600">{t('model.cropYield')}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-indigo-600 font-bold">🐛</span>
              <div>
                <p className="font-semibold text-gray-900">{t('model.stateAgricultureDept')}</p>
                <p className="text-gray-600">{t('model.pestIncidents')}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Info Button - Fixed at bottom right */}
      <div className="fixed bottom-6 right-6 z-20">
        <button
          onClick={() => setShowModelInfo(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-2xl transition-all hover:scale-110 flex items-center gap-2 group"
          title={t('model.info')}
        >
          <Info size={24} />
          <span className="max-w-0 overflow-hidden group-hover:max-w-xs transition-all duration-300 whitespace-nowrap font-medium">
            {t('model.info')}
          </span>
        </button>
      </div>

      {/* Model Info Modal */}
      <ModelInfoModal isOpen={showModelInfo} onClose={() => setShowModelInfo(false)} />
    </div>
  );
}

export default DashboardContent;
