import React, { useState } from 'react';
import { Leaf } from 'lucide-react';
import EnhancedSidebar from './components/EnhancedSidebar';
import DashboardContent from './components/DashboardContent';
import axios from 'axios';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [selectedValues, setSelectedValues] = useState(null);

  const API_BASE = '/api';

  const handleAnalyze = async (values) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await axios.post(`${API_BASE}/predict`, {
        state: values.state,
        district: values.district,
        crop: values.crop,
        season: values.season,
        soilType: values.soilType,
        landType: values.landType,
        sowingMonth: values.sowingMonth,
        farmSize: values.farmSize
      }, {
        timeout: 15000
      });

      setPrediction(response.data);
      setSelectedValues(values);
    } catch (err) {
      console.error('Prediction error:', err);
      const errorMsg = err.response?.data?.error || err.message || 'Failed to get prediction. Please try again.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-gradient-to-r from-green-700 to-emerald-600 text-white shadow-lg sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Leaf size={32} className="text-green-100" />
            <div>
              <h1 className="text-2xl font-bold">CFEWS</h1>
              <p className="text-green-100 text-sm">Crop Failure Early Warning System</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        <EnhancedSidebar onAnalyze={handleAnalyze} loading={loading} />
        <DashboardContent 
          prediction={prediction} 
          loading={loading} 
          error={error}
          selectedValues={selectedValues}
        />
      </div>
    </div>
  );
}

export default App;
