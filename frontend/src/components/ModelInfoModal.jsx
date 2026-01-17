import React, { useState, useEffect } from 'react';
import { X, Brain, Database, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

const ModelInfoModal = ({ isOpen, onClose }) => {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchModelInfo();
    }
  }, [isOpen]);

  const fetchModelInfo = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('http://localhost:5000/api/model-info');
      setModelInfo(response.data);
    } catch (err) {
      console.error('Failed to fetch model info:', err);
      setError('Failed to load model information');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-600 to-green-700 text-white p-6 rounded-t-lg flex justify-between items-center sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <Brain className="w-8 h-8" />
            <div>
              <h2 className="text-2xl font-bold">AI Model Information</h2>
              <p className="text-green-100 text-sm">Technical Details & Training Methodology</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-green-800 p-2 rounded-full transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
            </div>
          ) : error ? (
            <div className="flex items-center justify-center py-12 text-red-600">
              <AlertCircle className="w-6 h-6 mr-2" />
              <span>{error}</span>
            </div>
          ) : modelInfo ? (
            <div className="space-y-6">
              {/* Model Overview */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="text-xl font-bold text-green-800 mb-3 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  Model Overview
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Model Type</p>
                    <p className="font-semibold text-gray-800">{modelInfo.model_type}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Algorithm</p>
                    <p className="font-semibold text-gray-800">{modelInfo.algorithm}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Training Samples</p>
                    <p className="font-semibold text-gray-800">{modelInfo.training_samples} samples</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Test Split</p>
                    <p className="font-semibold text-gray-800">{modelInfo.test_split}</p>
                  </div>
                </div>
              </div>

              {/* Accuracy Card */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-300 rounded-lg p-6 text-center">
                <p className="text-gray-700 font-medium mb-2">Model Accuracy</p>
                <div className="text-6xl font-bold text-blue-600 mb-2">
                  {modelInfo.accuracy}%
                </div>
                <p className="text-sm text-gray-600">{modelInfo.accuracy_note}</p>
                <p className="text-sm text-gray-600 mt-2 italic">{modelInfo.validation_method}</p>
              </div>

              {/* Model Parameters */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-bold text-gray-800 mb-3">Model Parameters</h3>
                <div className="grid md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Number of Trees</p>
                    <p className="font-semibold text-gray-800">{modelInfo.n_estimators}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Max Tree Depth</p>
                    <p className="font-semibold text-gray-800">{modelInfo.max_depth}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Status</p>
                    <p className="font-semibold text-green-600">{modelInfo.model_status}</p>
                  </div>
                </div>
                {modelInfo.cv_mean && (
                  <div className="mt-4 pt-4 border-t border-gray-300">
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Cross-Validation Score</p>
                        <p className="font-semibold text-blue-600">{(modelInfo.cv_mean * 100).toFixed(2)}%</p>
                      </div>
                      {modelInfo.f1_score && (
                        <div>
                          <p className="text-gray-600">F1 Score</p>
                          <p className="font-semibold text-purple-600">{(modelInfo.f1_score * 100).toFixed(2)}%</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Model Enhancements */}
              {modelInfo.enhancements && modelInfo.enhancements.length > 0 && (
                <div className="bg-gradient-to-br from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4">
                  <h3 className="text-lg font-bold text-purple-800 mb-3">🚀 Recent Enhancements</h3>
                  <div className="space-y-2">
                    {modelInfo.enhancements.map((enhancement, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        <div className="w-5 h-5 bg-purple-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                          ✓
                        </div>
                        <span className="text-gray-700">{enhancement}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Input Features */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                  <Database className="w-5 h-5 text-green-600" />
                  Input Features ({modelInfo.features.length})
                </h3>
                <div className="grid md:grid-cols-2 gap-2">
                  {modelInfo.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center gap-2 bg-gray-50 p-2 rounded">
                      <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-xs font-bold">
                        {idx + 1}
                      </div>
                      <span className="text-sm text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Data Sources */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-bold text-gray-800 mb-3">Data Sources</h3>
                <div className="space-y-2">
                  {modelInfo.data_sources.map((source, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm">
                      <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{source}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Prediction Classes */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-bold text-gray-800 mb-3">Prediction Classes</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  {modelInfo.prediction_classes.map((cls, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg ${
                        idx === 0
                          ? 'bg-green-50 border border-green-300'
                          : 'bg-red-50 border border-red-300'
                      }`}
                    >
                      <p className={`font-semibold ${idx === 0 ? 'text-green-800' : 'text-red-800'}`}>
                        {cls}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Training Note */}
              <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-4">
                <p className="text-sm text-yellow-800">
                  <strong>Note:</strong> {modelInfo.training_note}
                </p>
              </div>

              {/* Disclaimer */}
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-4">
                <h3 className="text-sm font-bold text-gray-800 mb-2">DISCLAIMER</h3>
                <p className="text-xs text-gray-600 leading-relaxed">
                  This AI model provides risk predictions based on available data and should be used as a
                  guidance tool only. The accuracy may vary depending on data quality, regional conditions,
                  and unforeseen factors. Always consult with local agricultural extension officers,
                  agronomists, and experienced farmers before making final agricultural decisions. The
                  developers assume no liability for decisions made based on these predictions.
                </p>
              </div>
            </div>
          ) : null}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 rounded-b-lg border-t border-gray-200 flex justify-between items-center">
          <p className="text-sm text-gray-600">CFEWS v1.0 - Crop Failure Early Warning System</p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModelInfoModal;
